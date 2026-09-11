---
name: mathmodel-lit-review
description: "数模文献调研专家。输入题目或研究方向，生成检索词、多渠道检索论文（arXiv API、Semantic Scholar API、WebSearch 兜底），从论文中提取可借鉴的模型、算法与指标，产出 LITERATURE_REVIEW.md 与 references.bib 供建模、求解与论文引用。每条文献必须带可验证的 arXiv ID/DOI/URL。"
---

# 数模文献调研

本 skill 是"论文提供专家 + 论文信息提供专家"：从题目出发找论文、提炼可迁移的方法、沉淀可验证的参考文献。它**不推进建模流程**，只产出资产供其他工具消费——建模时读调研报告借鉴方法，写论文时用 `references.bib` 落引用。

## 硬性规则：文献真实性

- **每条文献必须带可验证标识**：arXiv ID（如 `2401.01234`）、DOI 或可访问 URL，三者至少其一。
- **写入报告前必须验证存在性**：用 WebFetch 打开该条目的 arXiv 页面或 DOI 链接确认论文真实存在、标题作者年份吻合。
- **禁止编造文献**：检索不到就如实说明"未找到相关文献"，不允许用貌似合理的标题/作者拼凑。
- 保留检索原文依据（搜索 API 返回的 JSON 存到 `literature/<题目>/search_raw/`），供追溯。

## 环境约定（运行 Python 前必读）

1. 读工作目录的 `.mathmodel_env.md` 获取 conda 环境约定；若无此文件或未设置，先询问用户用哪个 conda 环境（可运行 `conda env list` 列出候选），并将答案写入该文件。
2. 检索脚本只用 Python 标准库，**不需要安装任何包**。
3. 如遇缺包/缺工具，只报告并列出安装命令，**绝不擅自安装**。

## 工作流程

### Step 1: 拆解题目

从题目（或用户给的研究方向）提取：

- 关键词（中英双语）：领域词、方法词、场景词。
- 期望找到的论文类型：综述（了解全貌）、方法论文（可迁移算法）、应用论文（同类场景做法）。

### Step 2: 多路检索

优先用自带脚本做结构化检索（比裸搜可靠）：

```bash
# 按 .mathmodel_env.md 约定的环境运行（示例）
python <本 skill 目录>/scripts/search_papers.py --query "traffic flow prediction graph neural network" --source both --max-results 10 --out literature/<题目>/search_raw/round1.json
```

- `--source arxiv`：arXiv API（`export.arxiv.org/api/query`）
- `--source s2`：Semantic Scholar Graph API（`api.semanticscholar.org/graph/v1/paper/search`）
- `--source both`（默认）：两者都查，结果合并去重

脚本失败（网络/API 不可用）时，降级用 WebSearch 检索，并在报告中注明降级原因。中文文献（CNKI/万方）只能检索到索引层面，全文获取基本不可行，摘要层面的线索记录即可。

### Step 3: 筛选与精读（降级链，从轻到重）

**不要上来就下载 PDF**，按层级走，走到哪层够用就停：

| 层级 | 做法 | 适用场景 |
| --- | --- | --- |
| 1. 摘要 | 检索结果自带的摘要（arXiv abs 页/Semantic Scholar abstract 字段，WebFetch 抓取） | 初筛、判断相关性——绝大多数论文到此为止 |
| 2. HTML 全文 | 近年 arXiv 论文有 HTML 版：WebFetch 抓 `https://arxiv.org/html/<id>` | 需要看方法章节、公式、实验细节 |
| 3. 原生读 PDF | 老论文只有 PDF 版：下载到本地，用 Read 工具直接读（有文字层的 PDF 原生支持） | 必须看全文且无 HTML 版 |
| 4. 图像分析 | 扫描版 PDF（Read 返回图片占位符）：转图片后分析，或直接放弃全文只看摘要+图表 | 极少数情况 |
| 5. 放弃全文 | 记录"仅摘要层面" | 相关性边缘的文献 |

### Step 4: 方法提取（数模视角）

对入选文献逐篇提炼，写入调研报告：

- 核心模型/算法是什么（公式要点、流程概述）。
- 数据预处理与特征构造做法。
- 评价指标与验证方式（训练/验证划分、误差评估）。
- **可迁移到本题的切入点**：哪部分方法适合本题哪个子问题，为什么。

### Step 5: 产出资产

```text
literature/
  <题目名>/
    LITERATURE_REVIEW.md    # 文献清单 + 方法摘要 + 可借鉴点
    references.bib          # BibTeX 条目（已验证真实性）
    search_raw/             # 检索 API 原始返回，供追溯
```

`LITERATURE_REVIEW.md` 结构：

```markdown
# 文献调研：<题目名>

## 检索说明
检索词、数据源、日期、降级记录

## 文献清单
| # | 标题 | 作者/年份 | 标识(arXiv/DOI) | 相关性 | 层面 |

## 方法摘要（逐篇）
### <论文标题> [<标识>]
- 核心方法：
- 数据与指标：
- 可借鉴点：

## 给建模/求解的参考建议

## references.bib 条目清单
```

## 与其他工具的衔接

- `$mathmodel-modeling`：建模时读取 `LITERATURE_REVIEW.md` 借鉴方法（存在则读）。
- `$mathmodel-figures`：把文献中的算法伪代码落地为代码（存在则参考）。
- `$mathmodel-paper`：正文写"模型依据/相关工作"章节，并把 `references.bib` 条目按排版引擎转写进 `references.typ`（Hayagriva 语法）或 `references.tex`（BibTeX 语法）。
- `$mathmodel-verify`：检查正文引用与文献条目的一致性。

## 边界

- 只做检索、筛选、方法提取与文献资产管理；不建模、不跑实验、不写论文正文。
- 学术不端红线：不代写从论文整段搬运的内容，方法借鉴须改写表述并在论文中正确引用。
- Sci-Hub 等灰色渠道不碰；全文获取以官方开放渠道（arXiv 开放论文、Open Access）为准。
