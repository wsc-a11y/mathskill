# Figure Template Catalog（绘图模板目录）

统一模板目录，共 55 个：

- **seaborn 官方模板 49 个**（id 带 `sns-` 前缀）：代码原样收录自 seaborn 官方仓库 examples/，源码在 `references/seaborn-examples/`。使用 `sns.load_dataset()` 内置示例数据，定制时替换为用户真实数据即可。
- **补充模板 6 个**（matplotlib）：seaborn 覆盖不了的专业科研图，脚本在 `scripts/templates/`。

> **选图优先级（硬性规则）**：先在本目录的 seaborn 分区中找匹配图型，找到就必须用 seaborn 模板；仅当 seaborn 无对应图型、或数据确实更适合补充模板呈现时，才用「补充模板」分区。

渲染：`python scripts/render_template.py <id>`（`--list` 查看全部 id）。

## 单变量分布（看一个变量的形态）

| id | 图型 | 关键 API | 说明 |
| --- | --- | --- | --- |
| `sns-histogram-stacked` | 对数坐标堆叠直方图 | `sns.histplot` | 多组数据堆叠+对数刻度 |
| `sns-kde-ridgeplot` | 山脊图（重叠密度曲线） | `sns.kdeplot` + `FacetGrid` | 多组分布纵向重叠 |
| `sns-multiple-ecdf` | 分面经验累积分布（ECDF） | `sns.displot(kind="ecdf")` | 各组 ECDF 对比 |
| `sns-simple-violinplots` | 水平空心小提琴图 | `sns.violinplot` | 简洁单组分布 |
| `sns-wide-form-violinplot` | 宽表数据小提琴图 | `sns.violinplot` | 每列一个分布 |
| `sns-three-variable-histogram` | 三变量直方图 | `sns.displot` | 两分类变量分面+连续变量直方 |
| `sns-faceted-histogram` | 按子集分面直方图 | `sns.displot` | 按分类变量分面 |
| `sns-large-distributions` | 大样本分布图（letter-value） | `sns.boxenplot` | 尾部信息比箱线图更丰富 |

## 多变量/联合分布

| id | 图型 | 关键 API | 说明 |
| --- | --- | --- | --- |
| `sns-joint-histogram` | 联合分布+边缘直方图 | `sns.histplot` | 二元直方+两轴边缘 |
| `sns-joint-kde` | 联合 KDE 密度图 | `sns.jointplot` | 二元密度+边缘 |
| `sns-smooth-bivariate-kde` | 平滑二元 KDE+边缘直方图 | `sns.kdeplot` + `sns.histplot` | 更精细的联合分布 |
| `sns-multiple-bivariate-kde` | 多组二元 KDE | `sns.kdeplot` | 多组二维密度叠加 |
| `sns-multiple-conditional-kde` | 条件密度估计（分面） | `sns.displot` | 按条件变量分面的 KDE |
| `sns-hexbin-marginals` | 六边形聚合+边缘分布 | `sns.jointplot(kind="hex")` | 大数据量散点替代方案 |
| `sns-marginal-ticks` | 散点图+边缘刻度（rug） | `sns.scatterplot` + `sns.rugplot` | 在坐标轴边缘显示分布 |

## 变量关系（散点/相关矩阵）

| id | 图型 | 关键 API | 说明 |
| --- | --- | --- | --- |
| `sns-heat-scatter` | 散点热力图（密度着色） | `sns.relplot` | 密集散点按密度着色 |
| `sns-scatter-bubbles` | 气泡图（点大小+色调） | `sns.relplot` | 第三/四变量映射到大小和颜色 |
| `sns-scatterplot-sizes` | 连续色调+大小散点 | `sns.relplot` | 连续变量映射到色调和尺寸 |
| `sns-scatterplot-categorical` | 分类变量散点（swarm） | `sns.swarmplot` | 分类变量+连续变量关系 |
| `sns-different-scatter-variables` | 多样语义散点 | `sns.scatterplot` | 形状/颜色/大小全用上 |
| `sns-layered-bivariate-plot` | 分层二元图 | `sns.scatterplot` + `sns.kdeplot` + `sns.histplot` | 散点+KDE+直方多层叠加 |
| `sns-scatterplot-matrix` | 散点矩阵 | `sns.pairplot` | 多变量两两散点 |
| `sns-pair-grid-with-kde` | 配对密度+散点矩阵 | `PairGrid` | 对角 KDE+非对角散点 |
| `sns-pairgrid-dotplot` | 多变量点图矩阵 | `PairGrid` + `sns.stripplot` | 对角线分布+点图 |
| `sns-many-pairwise-correlations` | 对角相关矩阵热图 | `sns.heatmap` | 只画下三角相关矩阵 |

## 分类比较

| id | 图型 | 关键 API | 说明 |
| --- | --- | --- | --- |
| `sns-grouped-barplot` | 分组柱状图 | `sns.catplot(kind="bar")` | 两分类变量+连续变量 |
| `sns-part-whole-bars` | 水平条形图（部分-整体） | `sns.barplot` | 多组水平条形对比 |
| `sns-horizontal-boxplot` | 水平箱线图+观测散点 | `sns.boxplot` + `sns.stripplot` | 箱线+原始数据点 |
| `sns-grouped-boxplot` | 分组箱线图 | `sns.boxplot` | 两分类变量箱线 |
| `sns-grouped-violinplots` | 分组分裂小提琴图 | `sns.violinplot(split=True)` | 分组间分布对比 |
| `sns-jitter-stripplot` | 条件均值+抖动观测点 | `sns.stripplot` + `sns.pointplot` | 均值线+原始点 |
| `sns-paired-pointplots` | 配对分类点图 | `sns.pointplot` | 成对测量对比 |
| `sns-pointplot-anova` | 三因素 ANOVA 点图 | `sns.catplot` | 多因素均值对比 |

## 回归

| id | 图型 | 关键 API | 说明 |
| --- | --- | --- | --- |
| `sns-anscombes-quartet` | 安斯库姆四重奏 | `sns.lmplot` | 演示只看均值/方差会误判 |
| `sns-multiple-regression` | 多元线性回归分面 | `sns.lmplot` | 按类别分面回归线 |
| `sns-logistic-regression` | 分面逻辑回归 | `sns.lmplot(logistic=True)` | 二元结果概率曲线 |
| `sns-regression-marginals` | 回归+边缘分布 | `sns.jointplot(kind="reg")` | 回归线+两轴边缘 |
| `sns-strip-regplot` | 带状图上的回归拟合 | `sns.catplot` + `sns.regplot` | 分类变量上的回归线 |
| `sns-residplot` | 模型残差图 | `sns.residplot` | 残差诊断 |

## 时间序列与分面

| id | 图型 | 关键 API | 说明 |
| --- | --- | --- | --- |
| `sns-errorband-lineplots` | 误差带时序图 | `sns.lineplot` | 均值线+置信带 |
| `sns-faceted-lineplot` | 分面折线图 | `sns.relplot(kind="line")` | 多子集折线分面 |
| `sns-wide-data-lineplot` | 宽表折线图 | `sns.lineplot` | 每列一条线 |
| `sns-timeseries-facets` | 小多图时序（面积图） | `sns.relplot` | 多组时序面积 |
| `sns-many-facets` | 大量分面布局 | `FacetGrid` | 高分面数布局控制 |
| `sns-radial-facets` | 极坐标投影分面 | `FacetGrid` + polar | 径向分面图 |

## 热图与调色板

| id | 图型 | 关键 API | 说明 |
| --- | --- | --- | --- |
| `sns-spreadsheet-heatmap` | 带数值注释的热力图 | `sns.heatmap(annot=True)` | 表格型热图 |
| `sns-structured-heatmap` | 聚类结构热图 | `sns.clustermap` | 行列聚类热图 |
| `sns-palette-choices` | 调色板效果对比 | `sns.barplot` | 选色参考 |
| `sns-palette-generation` | cubehelix 调色板生成 | `sns.cubehelix_palette` | 自定义调色板 |

## 补充模板（seaborn 无对应图型时才用）

| id | 脚本 | 图型 |
| --- | --- | --- |
| `multiclass-shap-combo` | `make_multiclass_shap_combo.py` | 多分类 SHAP 柱状图与蜂群图组合图 |
| `cv-roc-ci` | `make_cv_roc_ci.py` | 交叉验证 ROC 曲线与置信区间图 |
| `taylor-diagram` | `make_taylor_diagram.py` | 多模型评价泰勒图 |
| `rf-tpe-surface` | `make_rf_tpe_surface.py` | TPE 优化 RF 模型 3D 曲面图 |
| `grouped-circular-heatmap` | `make_grouped_circular_heatmap.py` | 分组环形热图 |
| `nature-chord-diagram` | `make_nature_chord_diagram.py` | Nature 风格和弦图 |

Prompt 中包含 `$mathmodel-figure-templates` 与图型中文描述时，agent 应先将描述映射为上表 id 再调用 `scripts/render_template.py`。
