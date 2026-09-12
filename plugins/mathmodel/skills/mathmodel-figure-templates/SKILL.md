---
name: mathmodel-figure-templates
description: "科研绘图模板库。当用户要画数据图（散点、柱状、箱线、小提琴、直方、KDE、回归、热力图、相关矩阵、时序图等）时使用：优先从 49 个 seaborn 官方模板中选图（id 带 sns- 前缀，审美最佳）；seaborn 无对应图型（SHAP 蜂群、交叉验证 ROC、泰勒图、3D 曲面、环形热图、和弦图）时才用 6 个补充 matplotlib 模板。内置 55 个可直接运行的模板脚本。"
---

# 数模科研绘图模板库

内置 55 个开箱即跑的绘图模板，分两类：

1. **seaborn 官方模板 49 个**（主模板库，代码原样收录自 seaborn 官方仓库）：散点/柱状/箱线/小提琴/直方/KDE/回归/热力图/相关矩阵/时序等常规统计图，审美与规范最佳。
2. **补充 matplotlib 模板 6 个**：seaborn 覆盖不了的专业科研图。

渲染后输出 PNG/PDF/SVG 三格式，PDF 为矢量图适合论文。

## 选图优先级（硬性规则）

1. **先查 seaborn 官方模板**：打开 `references/figure-catalog.md`，在 seaborn 分区（id 带 `sns-` 前缀）中找匹配图型。**找到就必须用 seaborn 模板**，不得用补充模板或手写 matplotlib 替代。
2. **补充模板兜底**：仅当 seaborn 无对应图型（SHAP 蜂群、ROC+置信区间、泰勒图、3D 曲面、环形热图、和弦图），或用户数据确实更适合补充模板呈现时，才用「补充模板」分区。

## 环境约定（运行 Python 前必读）

1. 读工作目录的 `.mathmodel_env.md` 获取 conda 环境约定；若无此文件或未设置，先询问用户用哪个 conda 环境（可运行 `conda env list` 列出候选），并将答案写入该文件。
2. 依赖：seaborn 模板需要 `seaborn` + `pandas` + `matplotlib` + `numpy`（seaborn ≥ 0.13，示例使用 `bw_adjust` 等新 API）；补充模板只需 `matplotlib` + `numpy`。缺包时只报告并列出安装命令，**绝不擅自安装**。
3. seaborn 模板用 `sns.load_dataset()` 内置示例数据，**首次运行需联网下载**；离线失败时告知用户原因，或让用户提供数据替换。
4. 渲染器用当前 Python 解释器（`sys.executable`）执行模板脚本，激活了哪个 conda 环境就用哪个，无需手动指定解释器。

## 快速使用

1. 从 `references/figure-catalog.md` 找到目标图的模板 id（seaborn 模板以 `sns-` 开头）。
2. 定位渲染脚本：`<本 skill 目录>/scripts/render_template.py`。若不确定 skill 安装位置，先用 Glob 搜索 `render_template.py` 定位。
3. 运行：

```bash
python <本 skill 目录>/scripts/render_template.py sns-grouped-barplot
python <本 skill 目录>/scripts/render_template.py taylor-diagram
```

4. 渲染器把模板脚本复制到 `绘图复刻/scripts/`，运行后输出到 `绘图复刻/outputs/`（目录名可用 `--project` 修改）。
5. 把输出的 PNG/PDF/SVG 路径和复制的脚本路径告诉用户。

查看全部模板 id（55 个，分 seaborn / 补充两组显示）：

```bash
python <本 skill 目录>/scripts/render_template.py --list
```

## 输出约定

- 默认项目目录：`绘图复刻`（工作目录下）。
- 脚本路径：`绘图复刻/scripts/<模板文件名>.py`。
- 输出：`绘图复刻/outputs/<模板>_replica.png` / `.pdf` / `.svg`。
- 优先使用内置脚本原样渲染；用户要求定制时，先渲染一次再改 `绘图复刻/scripts/` 里的副本。

## 定制模板时

- **seaborn 模板**：把 `sns.load_dataset("...")` 替换为用户真实数据（DataFrame 结构保持列名一致），其余官方写法尽量保留；改 `绘图复刻/scripts/` 里的副本。
- **补充模板**：保留确定性随机种子（模拟数据可复现）、PNG/PDF/SVG 三格式导出、清晰的坐标轴与图例、高 DPI 输出。
- 实现模式参考 `references/plot-recipes.md`。

## 边界

- 模板用内置/模拟数据演示画法，**不要声称复现了某篇论文的真实数据**；换成用户真实数据时由用户确认数据口径。
- 本工具画"数据图表"；流程图、架构图等非数据图由 `$mathmodel-drawio` 负责。
