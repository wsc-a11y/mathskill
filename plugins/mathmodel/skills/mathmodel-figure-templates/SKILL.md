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

## 调色规则（硬性规则）

1. **默认用 seaborn 官方模板自带的颜色**，不加多余配色。
2. **颜色不够或需要整套配色时**（如模板只用 3 色但图需要 4 色），必须用 `scripts/pick_palette.py` 程序化选色，**禁止凭记忆/色环盲选**（凭感觉挑的色通常饱和度失控、色系打架）：
   - 低饱和淡色优先（顶刊论文配色）；默认 `top-journal` 风格。
   - 选好后**默认用户满意，直接画图**，不事前询问。
3. **用户看到成品图后不满意颜色时**：
   - 跑 `pick_palette.py` 生成**一批不同色系/风格的候选**（工具按色系多样性去重），用 `--preview` 出候选色板 PNG 给用户挑；
   - 用户选定某个候选后，用其 hex 重新配色画图；用户不满意不得坚持原色。
4. **用户对整批候选都不满意**：用 `--offset` 翻到下一批候选，直到用户满意。

```bash
python <本 skill 目录>/scripts/pick_palette.py --existing "#4C72B0 #DD8452 #55A868"   # 补色：3 色 → 推荐第 4 色
python <本 skill 目录>/scripts/pick_palette.py --n 4 --preview                         # 整套：4 色候选 + 色板预览 PNG
python <本 skill 目录>/scripts/pick_palette.py --n 4 --offset 5 --preview              # 用户不满意换下一批
python <本 skill 目录>/scripts/pick_palette.py --n 5 --kind sequential --preview        # 连续色板：热力图/3D 图/等高线
python <本 skill 目录>/scripts/pick_palette.py --n 5 --kind diverging --preview         # 发散色板：正负值/冷热/偏差对比
```

**按图表类型选 `--kind`**（默认 `qualitative`，选错会找不到合适候选）：

| 图表类型 | `--kind` |
| --- | --- |
| 柱状/折线/散点/箱线等**分类**图（各类别并列） | `qualitative`（默认） |
| 热力图、3D 曲面、等高线、密度图等**连续**量 | `sequential` |
| 正负值、冷热、偏差、距平类**双向**数据 | `diverging` |
| 拿不准 / 想在全部类型里搜 | `all`（候选会更杂，需自己判断） |

选出的 hex 直接用进绘图代码：`sns.set_palette([...])` 或 `palette=[...]`。

工具保证（已实现，勿绕过）：候选按**实际交付的前 N 色**评分，且这 N 色**全部通过填充色可用性检验**——近黑（明度 < 0.20）、近白（> 0.95）、近灰（饱和度 < 0.08）一律不作为填充色推荐。

**已知局限**：补色模式挑的是"离已有色最远"的颜色，结果可能偏深。嫌深时用 `--style vivid` 换风格，或该调色板整体不适用就换 `--offset` 下一批，不要手工去调那一个推荐色。

## 环境约定（运行 Python 前必读）

1. 读工作目录的 `.mathmodel_env.md` 获取 conda 环境约定；若无此文件或未设置，先询问用户用哪个 conda 环境（可运行 `conda env list` 列出候选），并将答案写入该文件。
2. **依赖**：seaborn 模板需 `seaborn` + `pandas` + `matplotlib` + `numpy`（seaborn ≥ 0.13，示例用了 `bw_adjust` 等新 API）；补充模板只需 `matplotlib` + `numpy`；选色工具需 `pypalettes`（无依赖纯 Python 包，`pip install pypalettes`）。缺包时只报告并列出安装命令，**绝不擅自安装**。

**关于 pypalettes**（0.2.1）：选色工具的**调色板数据源**，收录 1000+ 套调色板（来自 rcartocolor / wesanderson / MetBrewer 等 R 可视化包与科学期刊），每套附 `kind`（配色类型）与 `source`（出处）。`pick_palette.py` 已把它整体封装——**正常选色不需要直接调 pypalettes**，用 `--kind` / `--n` / `--style` 就够了。

只有下面两种情况才直接用它，用法（已实测）：

```python
import pypalettes

# ① 要某套具名色板的完整色值（如 Set1 / Dark2 / tab10）
pypalettes.load_palette("Set1", keep_first_n=4)   # ['#e41a1c','#377eb8','#4daf4a','#984ea3']
pypalettes.load_cmap("Set1").hex                  # 同上，另可取 .kind / .source

# ② 要按出处/风格筛选：直接读数据源 CSV
import importlib.resources, csv
f = importlib.resources.files("pypalettes").joinpath("palettes.csv")
rows = list(csv.DictReader(f.open(newline="", encoding="utf-8")))   # 列: name, palette, kind, source
```

直接使用时的坑（都实测过）：
- `load_palette()` **不传 name 会随机返回一套**，不是"默认色板"，要确定性就显式传名。
- 返回值**可能带 alpha**（形如 `'#366698FF'`，8 位）：喂给 matplotlib 多数场合可用，但自己解析 hex 时记得先截前 7 位。
- `get_kind` / `get_source` / `get_hex` **已废弃**（会告警），改用 `load_cmap("名").kind` / `.source` / `.hex`。
- `reverse=True` 是**反转后取前 N**（`load_palette("Set1", keep_first_n=3, reverse=True)` 返回 `['#e41a1c','#999999','#f781bf']`），不是"从末尾取 N 个"。
- 不是每套都有 kind：`load_cmap("Set1").kind` 返回**空字符串**。选色工具会跳过这类无类型的色板，若候选偏少属正常。
- `show_cmap("名")` 可直接画出色条，用于人工确认；选色工具自己的 `--preview` 更贴合选色流程，优先用后者。

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

模板 id 也支持中文关键词与别名（如「小提琴」「箱线」「泰勒」「和弦」），直接用中文描述图型也能匹配。

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
