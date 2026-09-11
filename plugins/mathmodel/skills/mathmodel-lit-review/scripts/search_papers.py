#!/usr/bin/env python3
"""数模文献检索脚本：查询 arXiv 与 Semantic Scholar，合并去重后输出 JSON。

仅使用 Python 标准库，无需安装任何第三方包。
"""
from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

ARXIV_API = "http://export.arxiv.org/api/query"
S2_API = "https://api.semanticscholar.org/graph/v1/paper/search"
S2_FIELDS = "title,abstract,year,authors,externalIds,url,venue"
TIMEOUT = 30

NS = {"atom": "http://www.w3.org/2005/Atom", "arxiv": "http://arxiv.org/schemas/atom"}


def fetch(url: str) -> bytes:
    """GET 请求，带 UA 与超时。"""
    req = urllib.request.Request(url, headers={"User-Agent": "mathmodel-lit-review/1.0"})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
        return resp.read()


def search_arxiv(query: str, max_results: int) -> tuple[list[dict], str | None]:
    """查询 arXiv API，返回统一条目列表；失败返回空列表和错误信息。"""
    params = urllib.parse.urlencode(
        {"search_query": f"all:{query}", "start": 0, "max_results": max_results}
    )
    try:
        raw = fetch(f"{ARXIV_API}?{params}")
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        return [], f"arXiv API 请求失败: {exc}"
    try:
        root = ET.fromstring(raw)
    except ET.ParseError as exc:
        return [], f"arXiv 返回解析失败: {exc}"
    papers = []
    for entry in root.findall("atom:entry", NS):
        title = (entry.findtext("atom:title", "", NS) or "").strip().replace("\n", " ")
        summary = (entry.findtext("atom:summary", "", NS) or "").strip().replace("\n", " ")
        authors = [a.findtext("atom:name", "", NS) or "" for a in entry.findall("atom:author", NS)]
        published = entry.findtext("atom:published", "", NS) or ""
        arxiv_id = (entry.findtext("atom:id", "", NS) or "").rsplit("/", 1)[-1]
        papers.append(
            {
                "title": title,
                "abstract": summary[:1500],
                "authors": authors,
                "year": published[:4],
                "arxiv_id": arxiv_id,
                "url": f"https://arxiv.org/abs/{arxiv_id}",
                "venue": "arXiv",
            }
        )
    return papers, None


def search_s2(query: str, max_results: int) -> tuple[list[dict], str | None]:
    """查询 Semantic Scholar API，返回统一条目列表；失败返回空列表和错误信息。

    S2 公共池有速率限制，遇到 429 退避重试两次。
    """
    params = urllib.parse.urlencode(
        {"query": query, "limit": max_results, "fields": S2_FIELDS}
    )
    url = f"{S2_API}?{params}"
    for attempt in range(3):
        try:
            raw = fetch(url)
            data = json.loads(raw)
        except (urllib.error.URLError, TimeoutError, OSError, json.JSONDecodeError) as exc:
            return [], f"Semantic Scholar 请求失败: {exc}"
        except urllib.error.HTTPError as exc:
            if exc.code == 429 and attempt < 2:
                time.sleep(5 * (attempt + 1))
                continue
            return [], f"Semantic Scholar HTTP {exc.code}"
        break
    papers = []
    for item in data.get("data", []):
        ext = item.get("externalIds") or {}
        papers.append(
            {
                "title": (item.get("title") or "").strip(),
                "abstract": (item.get("abstract") or "")[:1500],
                "authors": [(a.get("name") or "") for a in (item.get("authors") or [])],
                "year": str(item.get("year") or ""),
                "arxiv_id": ext.get("ArXiv") or "",
                "url": item.get("url") or "",
                "venue": item.get("venue") or "Semantic Scholar",
            }
        )
    return papers, None


def merge_papers(papers: list[dict]) -> list[dict]:
    """按 arXiv ID（缺失时按标题小写）去重合并。"""
    seen: set[str] = set()
    merged = []
    for p in papers:
        key = p["arxiv_id"].lower() if p["arxiv_id"] else p["title"].lower()
        if key and key in seen:
            continue
        seen.add(key)
        merged.append(p)
    return merged


def main() -> int:
    parser = argparse.ArgumentParser(description="数模文献检索：arXiv + Semantic Scholar")
    parser.add_argument("--query", required=True, help="检索词（英文效果最好）")
    parser.add_argument("--source", choices=["arxiv", "s2", "both"], default="both")
    parser.add_argument("--max-results", type=int, default=10)
    parser.add_argument("--out", help="输出 JSON 文件路径；不指定则打印到 stdout")
    args = parser.parse_args()

    papers: list[dict] = []
    errors: list[str] = []
    if args.source in ("arxiv", "both"):
        arxiv_papers, err = search_arxiv(args.query, args.max_results)
        papers.extend(arxiv_papers)
        if err:
            errors.append(err)
    if args.source in ("s2", "both"):
        s2_papers, err = search_s2(args.query, args.max_results)
        papers.extend(s2_papers)
        if err:
            errors.append(err)

    result = {
        "query": args.query,
        "source": args.source,
        "errors": errors,
        "count": 0,
        "papers": merge_papers(papers),
    }
    result["count"] = len(result["papers"])

    if args.out:
        out_path = Path(args.out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"已写入 {out_path}（{result['count']} 条）")
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
