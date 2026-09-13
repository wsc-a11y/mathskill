#!/usr/bin/env python3
"""PyPalettes 选色工具：为 seaborn 图补色 / 整套选色。

配合 SKILL.md「调色规则」：
- 默认低饱和（顶刊淡色）优先，通过饱和度惩罚实现；
- 候选按色系多样性去重，一批同时给出不同风格的配色供用户选择；
- 用户对整批不满意时用 --offset 翻到下一批候选。

依赖：pypalettes（无依赖纯 Python 包，pip install pypalettes）。
"""
from __future__ import annotations

import argparse
import ast
import csv
import importlib.resources
import math
from dataclasses import dataclass
from pathlib import Path

HUE_BUCKETS = [  # (名称, 色相区间起点, 终点)；近灰色单独归「中性」
    ("红", 345, 15),
    ("橙", 15, 45),
    ("黄", 45, 75),
    ("黄绿", 75, 105),
    ("绿", 105, 150),
    ("青", 150, 195),
    ("蓝", 195, 255),
    ("紫", 255, 285),
    ("品红", 285, 345),
]
MAX_RGB_DIST = math.sqrt(3 * 255**2)  # 归一化用
NEUTRAL_SAT_THRESHOLD = 0.08  # 平均饱和度低于此值视为无彩色系


@dataclass
class Palette:
    name: str
    colors: list[str]  # 不含 alpha 的 #RRGGBB
    kind: str
    source: str


def hex_to_rgb(hex_color: str) -> tuple[float, float, float]:
    hex_color = hex_color.strip().lstrip("#")
    return (
        int(hex_color[0:2], 16),
        int(hex_color[2:4], 16),
        int(hex_color[4:6], 16),
    )


def rgb_to_hsv(rgb: tuple[float, float, float]) -> tuple[float, float, float]:
    r, g, b = (v / 255 for v in rgb)
    mx, mn = max(r, g, b), min(r, g, b)
    d = mx - mn
    if d == 0:
        h = 0.0
    elif mx == r:
        h = 60 * (((g - b) / d) % 6)
    elif mx == g:
        h = 60 * ((b - r) / d + 2)
    else:
        h = 60 * ((r - g) / d + 4)
    s = 0.0 if mx == 0 else d / mx
    return h, s, mx


def rgb_dist(a: tuple[float, float, float], b: tuple[float, float, float]) -> float:
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))


def mean_saturation(colors: list[str]) -> float:
    return sum(rgb_to_hsv(hex_to_rgb(c))[1] for c in colors) / len(colors)


def hue_bucket(rgb: tuple[float, float, float]) -> str:
    h, s, _ = rgb_to_hsv(rgb)
    if s < NEUTRAL_SAT_THRESHOLD:  # 近灰色
        return "中性"
    return hue_name(h)


def hue_name(h: float) -> str:
    """按色相角度返回色系名，用于近灰判定之外的纯色相分桶。"""
    for name, lo, hi in HUE_BUCKETS:
        if lo < hi:
            if lo <= h < hi:
                return name
        else:  # 跨 0 度（红）
            if h >= lo or h < hi:
                return name
    return "中性"


def match_distance(palette: Palette, known_rgb: list[tuple[float, float, float]]) -> float:
    """已知颜色与调色板前 k 个颜色的一一最小匹配距离（归一化）。"""
    cand = [hex_to_rgb(c) for c in palette.colors[: len(known_rgb)]]
    used: set[int] = set()
    total = 0.0
    for k in known_rgb:
        best, best_i = float("inf"), -1
        for i, c in enumerate(cand):
            if i in used:
                continue
            d = rgb_dist(k, c)
            if d < best:
                best, best_i = d, i
        used.add(best_i)
        total += best
    return total / len(known_rgb) / MAX_RGB_DIST


def suggest_extra_color(palette: Palette, known_rgb: list[tuple[float, float, float]]) -> str | None:
    """从候选调色板的剩余颜色中挑补色：与已知色最小距离最大的颜色（保证区分度），
    排除近黑白灰（不可作填充色）。"""
    used = set(range(len(known_rgb)))
    best, best_color = -1.0, None
    for i, color in enumerate(palette.colors):
        if i in used or not is_fill_color(color):
            continue
        rgb = hex_to_rgb(color)
        min_d = min(rgb_dist(rgb, k) for k in known_rgb)
        if min_d > best:
            best, best_color = min_d, color
    return best_color


def load_palettes() -> list[Palette]:
    with importlib.resources.files("pypalettes").joinpath("palettes.csv").open(
        newline="", encoding="utf-8"
    ) as f:
        rows = list(csv.DictReader(f))
    palettes = []
    for row in rows:
        try:
            colors = [c[:7] for c in ast.literal_eval(row["palette"])]  # 去 alpha
        except (ValueError, SyntaxError):
            continue
        if len(colors) < 2:
            continue
        palettes.append(Palette(row["name"], colors, row["kind"], row["source"]))
    return palettes


SAT_TARGET = 0.35  # 顶刊淡色的目标平均饱和度：有彩低饱和，不是灰也不是艳
MIN_SAT = 0.08  # 低于此值近灰：作填充色无法与背景及彼此区分
MIN_VALUE = 0.20  # 低于此值近黑：作填充色与文字/边框糊成一片
MAX_VALUE = 0.95  # 高于此值近白：作填充色印出来几乎看不见


def is_fill_color(color: str) -> bool:
    """判断该色能否用作填充色（排除近黑、近白、近灰）。"""
    _, s, v = rgb_to_hsv(hex_to_rgb(color))
    return s >= MIN_SAT and MIN_VALUE <= v <= MAX_VALUE


def score_palette(
    palette: Palette,
    known_rgb: list[tuple[float, float, float]],
    style: str,
    need: int,
) -> float | None:
    """补色模式：匹配距离优先（色差过大返回 None 排除），离目标饱和度越近越优先；
    整套模式：vivid 越高饱和越优先，否则离目标饱和度越近越优先。

    饱和度只统计**实际会交付的前 need 色**，且这些色必须都能作填充色。
    用整条调色板评分会排出「整条达标、交付色掺灰」的劣质候选。
    """
    used = palette.colors[:need]
    if any(not is_fill_color(c) for c in used):
        return None
    mean_sat = mean_saturation(used)
    sat_term = -mean_sat if style == "vivid" else abs(mean_sat - SAT_TARGET)
    if known_rgb:
        d = match_distance(palette, known_rgb)
        if d > 0.4:  # 与已知色系差太远，不协调，排除
            return None
        return d + 0.4 * sat_term
    return sat_term


def diversify(
    candidates: list[tuple[float, Palette]],
    known_rgb: list[tuple[float, float, float]],
    need: int,
) -> list[tuple[float, Palette]]:
    """按候选自身主导色相分桶去重：每个色系只保留分数最低的 1 个，一批同时给出不同风格。

    主导色相取自**实际交付的前 need 色**，与 score_palette 的评分口径保持一致。
    """
    buckets: dict[str, tuple[float, Palette]] = {}
    for score, pal in candidates:
        used = pal.colors[:need]
        h = sum(rgb_to_hsv(hex_to_rgb(c))[0] for c in used) / len(used)
        bucket = hue_name(h)
        if bucket not in buckets or score < buckets[bucket][0]:
            buckets[bucket] = (score, pal)
    return sorted(buckets.values())


def render_preview(
    candidates: list[tuple[float, Palette]], out: Path, known_colors: list[str]
) -> None:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    n = len(candidates)
    fig, ax = plt.subplots(figsize=(10, max(1.6, 0.75 * n + 1.2)))
    ax.set_xlim(0, 11)
    ax.set_ylim(-0.2, n + (0.9 if known_colors else 0))
    ax.axis("off")

    if known_colors:
        for i, c in enumerate(known_colors):
            ax.add_patch(plt.Rectangle((i * 0.7, n + 0.05), 0.6, 0.45, color=c, ec="#cccccc"))
        ax.text(0, n + 0.62, "Known colors (seaborn template)", fontsize=8, va="bottom")

    for idx, (score, pal) in enumerate(candidates):
        row = n - 1 - idx
        for i, c in enumerate(pal.colors[: max(8, len(known_colors) + 1)]):
            ax.add_patch(plt.Rectangle((i * 0.7, row), 0.6, 0.5, color=c, ec="#cccccc"))
        label = f"{pal.name}  ({pal.kind}, {len(pal.colors)} colors)  score={score:.3f}"
        ax.text(len(pal.colors) * 0.7 + 0.3, row + 0.25, label, fontsize=8, va="center")

    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Preview: {out}")


def main() -> None:
    parser = argparse.ArgumentParser(description="PyPalettes 选色：seaborn 图补色 / 整套选色")
    parser.add_argument("--n", type=int, help="整套模式：需要的颜色数")
    parser.add_argument("--existing", help='补色模式：已知颜色 hex，空格分隔，如 "#4C72B0 #55A868 #C44E52"')
    parser.add_argument("--kind", default="qualitative",
                        help="调色板类型：qualitative(默认)/sequential/diverging/all")
    parser.add_argument("--style", default="top-journal", choices=["top-journal", "vivid"],
                        help="top-journal=低饱和淡色优先（顶刊配色，默认）；vivid=高饱和鲜艳")
    parser.add_argument("--top", type=int, default=5, help="每批候选数量，默认 5")
    parser.add_argument("--offset", type=int, default=0, help="翻页：跳过前 N 个候选（用户对整批不满意时换一批）")
    parser.add_argument("--preview", action="store_true", help="渲染色板预览 PNG")
    parser.add_argument("--out", default="palette_preview.png", help="预览 PNG 输出路径")
    args = parser.parse_args()

    existing = args.existing.split() if args.existing else []
    known_rgb = [hex_to_rgb(c) for c in existing]
    need = args.n or (len(existing) + 1)

    palettes = load_palettes()
    pool = []
    for pal in palettes:
        if args.kind != "all":
            kinds = {pal.kind, pal.kind.split("-")[0]}
            if args.kind not in kinds:
                continue
        if len(pal.colors) < need:
            continue
        if existing and len(pal.colors) < len(existing) + 1:
            continue
        if mean_saturation(pal.colors) < 0.12:  # 灰系排除，顶刊淡色是有彩低饱和而非灰色
            continue
        s = score_palette(pal, known_rgb, args.style, need)
        if s is None:
            continue
        pool.append((s, pal))

    candidates = diversify(pool, known_rgb, need)[args.offset : args.offset + args.top]
    if not candidates:
        raise SystemExit("没有找到符合要求的调色板，试试 --kind all 或减少颜色数")

    style_name = "低饱和淡色（顶刊）" if args.style == "top-journal" else "高饱和鲜艳"
    print(f"风格: {style_name} | 类型: {args.kind} | 需要 {need} 色")
    if existing:
        print(f"已知颜色: {' '.join(existing)}")
    print("-" * 60)
    for i, (score, pal) in enumerate(candidates, start=args.offset + 1):
        shown = pal.colors[:need]
        print(f"[{i}] {pal.name}  ({pal.kind}, 共{len(pal.colors)}色)  score={score:.3f}")
        print(f"    {' '.join(shown)}")
        if existing:
            extra = suggest_extra_color(pal, known_rgb)
            if extra:
                print(f"    推荐补色: {extra}")
        print(f"    来源: {pal.source}")
    print("-" * 60)
    print(f"对整批不满意？用 --offset {args.offset + args.top} 看下一批不同色系候选。")

    if args.preview:
        render_preview(candidates, Path(args.out), existing)


if __name__ == "__main__":
    main()
