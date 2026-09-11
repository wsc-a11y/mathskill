---
name: mathmodel-init
description: "数学建模项目脚手架。用于初始化数模工作目录：创建标准目录结构（reports/code/results/figures/paper）和环境约定文件 .mathmodel_env.md，记录 conda 环境与论文偏好。本 skill 不编排流程，各阶段工具（建模、画图、论文等）由用户按需单独触发。"
---

# 数模项目脚手架

本 skill 只做一件事：把当前工作目录初始化为数模项目标准结构，并建立环境约定文件。它**不编排流程**——建模、画图、写论文等工具由用户按需单独触发（如 `$mathmodel-modeling`、`$mathmodel-figures`、`$mathmodel-paper`）。

## 必须产出

在当前工作目录创建或更新：

- `.mathmodel_env.md`：环境约定文件（conda 环境、论文偏好）。
- `reports/`：各工具的报告目录。
- `code/` 与 `code/outputs/`：求解代码与中间数据。
- `results/`：结果记录。
- `figures/`：所有图表（数据图 PDF + 非数据图 drawio/PDF）。
- `paper/`：论文目录（`main.typ` 或 `main.tex` + `sections/`）。

## 工作流程

### Step 1: 检查现状

若骨架目录和 `.mathmodel_env.md` 已存在，只补缺失项，不覆盖已有约定。

### Step 2: 创建目录骨架

```text
.
├── .mathmodel_env.md            # 本文件的环境约定
├── reports/                     # 各工具产出报告
├── code/                        # 求解代码（mathmodel-figures）
│   └── outputs/                 # 中间数据（清洗摘要、迭代历史等）
├── results/                     # 结果记录（mathmodel-figures）
├── figures/                     # 所有图表（mathmodel-figures + mathmodel-drawio）
└── paper/                       # 论文（mathmodel-paper）
    └── sections/
```

### Step 3: 询问并记录环境约定

以对话方式询问用户（未设置的项才问）：

1. **conda 环境**：运行 Python 用哪个环境？（执行 `conda env list` 列出候选，让用户选择；用户环境未用 conda 则记为"系统 Python"）
2. **排版引擎**：Typst 还是 LaTeX？（决定 mathmodel-paper 的模板与编译命令）
3. **竞赛类型**：国赛/华为杯/华中杯/MCM/...（决定论文模板族）
4. **论文语言**：中文/英文

写入 `.mathmodel_env.md`：

```markdown
# 环境约定（mathmodel-init 创建，各工具运行时读取）

## Python
conda 环境: <环境名或"系统 Python">   # 运行 Python 前激活：conda activate <环境名>

## 论文偏好（mathmodel-paper 使用）
排版引擎: <Typst / LaTeX>
竞赛类型: <国赛 / 华为杯 / MCM / ...>
论文语言: <中文 / 英文>
```

### Step 4: 说明目录分工

| 目录/文件 | 用途 | 主要使用者 |
| --- | --- | --- |
| `.mathmodel_env.md` | 环境约定（conda、论文偏好） | 所有工具 |
| `reports/` | 各阶段报告（建模、结果、图示、文献、验收） | 全部 |
| `code/`、`code/outputs/` | 求解代码与中间数据 | `$mathmodel-figures` |
| `results/` | 结果记录 | `$mathmodel-figures` |
| `figures/` | 数据图 + 非数据图 | `$mathmodel-figures`、`$mathmodel-drawio` |
| `paper/` | 论文主文件与章节 | `$mathmodel-paper` |

## 工具分工总览

各工具独立触发，无先后依赖；按需组合即可：

| 工具 | 作用 | 主要产物 |
| --- | --- | --- |
| `$mathmodel-modeling` | 赛题分析、变量/约束识别、建立模型、目标函数与求解策略 | `reports/ANALYSIS_MODELING_REPORT.md` |
| `$mathmodel-figures` | 实现可复现代码、运行实验、生成结果表与数据图表 | `code/`、`results/`、`reports/RESULTS_REPORT.md`、`figures/数据图` |
| `$mathmodel-drawio` | 技术路线图、算法流程图、模型结构图等非数据图 | `figures/*.drawio`、`figures/*.pdf`、`reports/DRAWIO_REPORT.md` |
| `$mathmodel-paper` | 撰写竞赛论文并按章节插入图表与文献引用 | `paper/` |
| `$mathmodel-verify` | 论文验收：结构、图表引用、数值一致性、编译、提交就绪 | `reports/VERIFY_REPORT.md` |
| `$mathmodel-lit-review` | 文献调研：从论文中提取可借鉴方法与参考文献 | `literature/`、`reports/LITERATURE_REVIEW.md` |
| `$mathmodel-figure-templates` | 科研绘图模板复刻（SHAP 组合图、泰勒图、和弦图等 11 种） | 用户指定输出目录 |
| `$mathmodel-doctor` | 环境检查与安装向导 | 检查报告 |

## 注意事项

- 不写 `plan.md`、`todo.md`，不做阶段调度。
- 目录骨架只是默认约定，用户已有目录结构时以现有结构为准。
- `.mathmodel_env.md` 是"问一次、全家共享"的机制：各工具运行前先读它，未设置才询问用户。
