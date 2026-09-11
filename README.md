# MathModel 数模工具箱（Codex 插件）

面向数学建模竞赛（国赛 / MCM / 华为杯 / 华中杯等）的**离散工具集**：不做全流程编排，每个工具独立触发、按需组合。你说"现在我要画图"，就只调画图工具。

## 安装

### 方式一：作为 Codex 插件安装（推荐）

**从 GitHub 安装**（仓库发布后）：

```bash
codex plugin marketplace add <owner>/<repo>@main
# 或 HTTPS 地址：codex plugin marketplace add https://github.com/<owner>/<repo>
codex plugin add mathmodel
```

**从本地目录安装**（克隆到本地后）：

```bash
codex plugin marketplace add <本仓库本地路径>
codex plugin add mathmodel -m mathmodel-marketplace
```

安装后 10 个 skill 自动可用；可用 `codex plugin list` 查看状态。

### 方式二：手动安装 skills（兜底）

把插件内的 skills 直接复制到 Codex 用户级目录：

```bash
# Windows（Git Bash）
cp -r plugins/mathmodel/skills/* ~/.codex/skills/
```

安装后重启 Codex 重新索引。若 `$mathmodel-xxx` 不生效，检查 `~/.agents/skills/` 是否是你的版本所用路径。

## 工具清单

| 工具 | 用途 | 触发示例 |
| --- | --- | --- |
| `$mathmodel-init` | 初始化数模项目骨架 + 环境约定文件 | "初始化一个数模项目" |
| `$mathmodel-modeling` | 赛题分析、拆子问题、建模型、写建模报告 | "给这道题建模" |
| `$mathmodel-figures` | 编程求解、跑实验、出结果表和数据图 | "把模型跑出来并画图" |
| `$mathmodel-drawio` | 技术路线图、流程图、模型结构图等非数据图 | "画个求解流程图" |
| `$mathmodel-paper` | 论文撰写（Typst/LaTeX 双引擎 + 14 中 3 英模板）+ 文献引用落地 | "写论文" |
| `$mathmodel-verify` | 论文验收：结构、引用、数值一致性、编译 | "检查论文" |
| `$mathmodel-lit-review` | 文献调研：检索论文、提取方法、产出参考文献 | "找找这题的论文和方法" |
| `$mathmodel-figure-templates` | 11 种科研绘图模板（SHAP 组合图、泰勒图、和弦图等） | "画个云雨图" |
| `$mathmodel-doctor` | 环境检查与安装向导（支持 conda） | "检查环境" |

## 环境要求

- Python 3.10+（推荐 conda 环境；`matplotlib` + `numpy` 即可画图，建模求解另需 `pandas`/`scipy`/`scikit-learn`/`openpyxl`）
- 论文编译：`typst` 或 `xelatex`（至少一个）
- 流程图导出 PDF：`drawio` CLI（可选）
- 论文验收视觉检查：`pdftoppm`/`mutool`/`magick` 任一（可选）

跑一次 `$mathmodel-doctor` 即可检查全部依赖并获取安装命令。

## 环境约定文件（问一次，全家共享）

`$mathmodel-init` 会在工作目录创建 `.mathmodel_env.md`：

```markdown
# 环境约定（mathmodel-init 创建，各工具运行时读取）

## Python
conda 环境: <环境名或"系统 Python">

## 论文偏好（mathmodel-paper 使用）
排版引擎: <Typst / LaTeX>
竞赛类型: <国赛 / 华为杯 / MCM / ...>
论文语言: <中文 / 英文>
```

所有工具运行前先读它：有约定就静默遵守，没有才询问用户。**任何工具都不会擅自安装包**，缺依赖只报告并给出命令。

## 工作目录约定

各工具的全部产物都在你的**工作目录**内（不写系统目录）：

```text
.
├── .mathmodel_env.md        # 环境约定
├── reports/                 # 建模/结果/图示/文献/验收报告
├── code/、code/outputs/     # 求解代码与中间数据
├── results/                 # 结果记录
├── figures/                 # 数据图 PDF + 非数据图 drawio/PDF
├── paper/                   # 论文
└── literature/<题目>/       # 文献调研资产（含 references.bib）
```

## 典型用法

离散组合，按需触发：

1. "初始化一个数模项目" → `$mathmodel-init`（建骨架、记 conda 与论文偏好）
2. "找找这道题可借鉴的论文" → `$mathmodel-lit-review`（产出调研报告 + references.bib）
3. "给这道题建模" → `$mathmodel-modeling`（写建模报告，参考调研报告）
4. "把模型跑出来并画图" → `$mathmodel-figures`（出结果报告 + 数据图）
5. "画个技术路线图" → `$mathmodel-drawio`
6. "写论文" → `$mathmodel-paper`（落图表 + 落引用）
7. "检查论文" → `$mathmodel-verify`

每一步都可以跳过、重跑或单独使用。

## 说明

- 绘图模板（`$mathmodel-figure-templates`）使用确定性模拟数据演示画法，换真实数据时以用户数据口径为准。
- 文献调研只从官方开放渠道（arXiv、Semantic Scholar 等）获取论文，每条文献必须可验证，禁止编造。
- 本仓库基于 MathModelAgent 项目的 skills 资产改造而来（离散化 + Codex 适配）。

## License

MIT
