---
name: mathmodel-figure-templates
description: "科研绘图模板库。当用户要画 SHAP 蜂群柱状图、配对云雨图、交叉验证 ROC、泰勒图、相关矩阵组合图、预测真实值边缘分布图、TPE 调参 3D 曲面、下三角相关矩阵半边小提琴图、分组环形热图、城市公园降温组合图或 Nature 和弦图时使用。内置 11 个可直接运行的 matplotlib 模板脚本。"
---

# 数模科研绘图模板库

内置 11 个开箱即跑的 matplotlib 科研绘图模板（确定性模拟数据，可复制改造为真实数据版本）。渲染后输出 PNG/PDF/SVG 三格式，PDF 为矢量图适合论文。

## 环境约定（运行 Python 前必读）

1. 读工作目录的 `.mathmodel_env.md` 获取 conda 环境约定；若无此文件或未设置，先询问用户用哪个 conda 环境（可运行 `conda env list` 列出候选），并将答案写入该文件。
2. 依赖只有 `matplotlib` + `numpy`。缺包时只报告并列出安装命令，**绝不擅自安装**。
3. 渲染器用当前 Python 解释器（`sys.executable`）执行模板脚本，激活了哪个 conda 环境就用哪个，无需手动指定解释器。

## 快速使用

1. 从 `references/figure-catalog.md` 找到目标图的模板 id。
2. 定位渲染脚本：`<本 skill 目录>/scripts/render_template.py`。若不确定 skill 安装位置，先用 Glob 搜索 `render_template.py` 定位。
3. 运行：

```bash
python <本 skill 目录>/scripts/render_template.py paired-raincloud
```

4. 渲染器把模板脚本复制到 `绘图复刻/scripts/`，运行后输出到 `绘图复刻/outputs/`（目录名可用 `--project` 修改）。
5. 把输出的 PNG/PDF/SVG 路径和复制的脚本路径告诉用户。

查看全部模板 id：

```bash
python <本 skill 目录>/scripts/render_template.py --list
```

## 输出约定

- 默认项目目录：`绘图复刻`（工作目录下）。
- 脚本路径：`绘图复刻/scripts/make_<模板>.py`。
- 输出：`绘图复刻/outputs/<模板>_replica.png` / `.pdf` / `.svg`。
- 优先使用内置脚本原样渲染；用户要求定制时，先渲染一次再改 `绘图复刻/scripts/` 里的副本。

## 模板 id 清单

- `multiclass-shap-combo` — 多分类 SHAP 柱状图与蜂群图组合图
- `paired-raincloud` — 配对云雨图
- `cv-roc-ci` — 交叉验证 ROC 曲线与置信区间图
- `taylor-diagram` — 多模型评价泰勒图
- `correlation-pairgrid` — 数据分布+拟合线+置信区间+相关系数组合图
- `prediction-marginal-grid` — 预测值与真实值边缘分布组合图
- `rf-tpe-surface` — TPE 优化 RF 模型 3D 曲面图
- `grouped-corr-split-violin` — 下三角相关矩阵 + 特征分组半边小提琴图
- `grouped-circular-heatmap` — 分组环形热图
- `urban-park-cooling-combo` — 堆叠图 + 云雨图 + 箱线图组合图
- `nature-chord-diagram` — Nature 风格和弦图

## 定制模板时

改 `绘图复刻/scripts/` 里的副本，保留：

- 确定性随机种子（模拟数据可复现）。
- PNG/PDF/SVG 三格式导出。
- 清晰的坐标轴、图例和高 DPI 输出。

实现模式参考 `references/plot-recipes.md`。

## 边界

- 模板用模拟数据演示画法，**不要声称复现了某篇论文的真实数据**；换成用户真实数据时由用户确认数据口径。
- 本工具画"漂亮图表"；流程图、架构图等非数据图由 `$mathmodel-drawio` 负责。
