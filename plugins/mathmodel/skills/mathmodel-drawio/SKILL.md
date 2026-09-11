---
name: mathmodel-drawio
description: "数学建模非数据型图示绘制工具。根据 ANALYSIS_MODELING_REPORT.md、RESULTS_REPORT.md 和已有 figures/（或用户描述）生成技术路线图、子问题求解流程图、模型结构图、数据处理流程图等 DrawIO 图，并导出论文可引用 PDF。可独立触发。"
---

# DrawIO 非数据图示绘制

本工具只负责论文中的**非数据型图示**，例如技术路线图、求解流程图、模型结构图、数据处理流程图、变量关系图、指标体系图等。前序报告文件存在则读取，不存在时以用户描述为准。

## 数学建模规范参考

如需领域判断，读取 `../mathmodel-references/math_modeling_norms.md` 中的“图表与可视化”和“非数据图工具选择”小节。该文件只作为规范知识库，不要求为了凑数量生成额外图示。

## 边界

- 负责：DrawIO 源文件、非数据图 PDF、图示生成记录。
- 不负责：折线图、柱状图、散点图、热力图、箱线图、雷达图等数据图。这些由 `$mathmodel-figures` 生成。
- 不重跑模型、不修改 `code/`，不改写 `reports/RESULTS_REPORT.md` 的数值结论。

## 必须产出

在当前工作目录创建或更新：

```text
figures/
  fig_roadmap.drawio
  fig_roadmap.pdf
  fig_flow_q1.drawio
  fig_flow_q1.pdf
  ...
reports/DRAWIO_REPORT.md
```

如果某类图不需要生成，必须在 `reports/DRAWIO_REPORT.md` 中说明原因。竞赛论文通常至少需要一张 `fig_roadmap` 技术路线图。

读取这些文件的目的不是提取数据作图，而是理解论文方法、章节结构、子问题关系和已有图表，避免重复。

## 工作流程

### Step 1: 盘点已有图表和需求

先读取以下文件（存在则读取）：`reports/ANALYSIS_MODELING_REPORT.md`、`reports/RESULTS_REPORT.md`、`figures/` 目录列表。

然后从前序文档提取非数据图需求，输出一个清单：

```text
DRAWIO PLAN CHECKLIST:
[ ] fig_roadmap      技术路线图，放在问题重述/绪论
[ ] fig_flow_q1      问题一求解流程图
[ ] fig_flow_q2      问题二求解流程图
[ ] fig_flow_q3      问题三求解流程图
[ ] fig_pipeline     数据处理流程图
[ ] fig_model        模型结构/变量关系图
```

清单不是固定模板，要根据题目实际删减或增补。不要为了凑图生成无意义图示。

**图文比阈值参考**（判断"该有图但没图"的空白区域；来源：顶级期刊图表规范 v3.0 智能补图模块）：

| 章节类型 | 阈值 |
| --- | --- |
| 问题分析/模型建立 | 字数/图片数 > 800 → 需要补流程图/框架图 |
| 结果分析 | > 500 → 需要补数据对比图（数据图由 `$mathmodel-figures` 负责） |
| 灵敏度/参数分析 | > 400 → 需要补热力图/雷达图（数据图由 `$mathmodel-figures` 负责） |
| 前言/背景 | > 1000 → 可选补图 |
| 结论 | 一般不补图（除非有总结性数据对比） |

不触发场景：已有同类型图覆盖、纯理论推导难以可视化、已有公式/表格充分表达、综述性质无具体数据——不强行补图。

### Step 2: 判定图类型

常见图示选择：

| 图类型 | 文件名建议 | 适用场景 |
| --- | --- | --- |
| 技术路线图 | `fig_roadmap` | 展示整体解题路线、章节逻辑、方法串联 |
| 子问题求解流程图 | `fig_flow_q1`, `fig_flow_q2` | 展示单个子问题的输入、判断、算法、输出 |
| 数据处理流程图 | `fig_pipeline` | 展示数据清洗、特征构造、建模输入 |
| 模型结构图 | `fig_model` | 展示模块关系、变量关系、模型层次 |
| 指标体系图 | `fig_index_system` | 展示目标层、准则层、指标层 |
| 决策树/规则图 | `fig_decision_tree` | 展示分类规则、设备选择、策略分支 |

不要用 DrawIO 画这些图：

- 结果对比柱状图
- 预测误差曲线
- 灵敏度曲线
- 相关性热力图
- 分布图和箱线图

### Step 3: 生成 DrawIO 源文件

每张图一个 `.drawio` 文件，放在 `figures/`。

DrawIO 内容要求：

- 文字语言与论文语言一致。
- 节点文字短，必要时双行，不堆长句。
- 同类节点样式统一。
- 箭头方向清晰，避免交叉。
- 图中不写大段解释，解释留给论文正文。
- 不使用装饰性阴影和过度渐变。

**节点形状-语义-配色对照表**（来源：顶级期刊图表规范 v3.0 流程图规范；所有流程图/架构图/路线图统一遵守）：

| 语义 | 节点形状 | 填充色 | 边框色 |
| --- | --- | --- | --- |
| 输入数据/已知条件 | 平行四边形 | #E3F2FD | #1565C0 |
| 分析步骤/处理过程 | 圆角矩形 | #E8F5E9 | #2E7D32 |
| 决策判断/条件分支 | 菱形 | #FFF3E0 | #E65100 |
| 模型/算法模块 | 矩形 | #F3E5F5 | #6A1B9A |
| 输出结果/结论 | 圆角矩形（加粗边框） | #FCE4EC | #AD1457 |
| 反馈/迭代回路 | 虚线箭头 | — | #333333 |
| 章节分区 | 虚线圆角矩形外框（极淡色） | alpha=0.3 | — |

补充要求（同来源）：

- 节点文字 ≤ 8 个词，核心动词开头（如「提取特征」「构建模型」「求解优化」）。
- 主流程方向全图统一（自上而下或自左向右）。
- 至少划分 2-3 个分区（如「数据输入」「模型构建」「结果输出」），每区独立配色。
- 箭头标注流向语义（输入/输出/反馈/迭代），非简单连接。

生成大 XML 时，分段写入，避免截断。示例：

```bash
mkdir -p figures
cat << 'XMLEOF' > figures/fig_roadmap.drawio
<mxfile>
  <diagram name="Page-1">
    <mxGraphModel>
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
        <!-- nodes and edges -->
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
XMLEOF
```

### Step 4: 导出 PDF

优先用可用的 DrawIO 命令导出 PDF：

```bash
DRAWIO_BIN="$(command -v drawio 2>/dev/null || command -v draw.io 2>/dev/null || command -v draw.io.exe 2>/dev/null || true)"
if [ -n "$DRAWIO_BIN" ]; then
  "$DRAWIO_BIN" --export --format pdf --crop --output figures/fig_roadmap.pdf figures/fig_roadmap.drawio
else
  echo "DrawIO command not found; keep .drawio source and record export failure."
fi
```

如果无法导出 PDF，保留 `.drawio`，在 `reports/DRAWIO_REPORT.md` 记录失败原因和建议导出命令。

### Step 5: 自检和修复

每张图必须检查：

- `.drawio` 文件非空。
- 若导出成功，`.pdf` 文件非空。
- 节点没有明显重叠。
- 箭头不穿过核心节点。
- 字号、颜色、边框风格一致。
- 文件名和图意一致。
- 没有与 `mathmodel-figures` 的数据图重复。

发现问题要修 `.drawio` 并重新导出，不要只在报告里解释。

### Step 6: 写生成记录

创建 `reports/DRAWIO_REPORT.md`，至少包含：

```markdown
# DrawIO 图示生成报告

## 图示清单
| 文件 | 类型 | 来源依据 | 用途 | 状态 |
| --- | --- | --- | --- | --- |

## 未生成图示及原因

## 导出与自检记录

## 给论文阶段的嵌入建议
```

嵌入建议只说明每张图适合放入哪个章节和建议 caption，不生成 `*_typst_includes.typ`。最终的图表插入代码（Typst 的 `#figure(image(...), caption: [...])` 或 LaTeX 的 `\begin{figure}...\end{figure}`）由 `mathmodel-paper` 根据论文结构和所选引擎决定。

## 质量要求

- 图示服务论文论证，不为装饰而画。
- 每张图必须能对应到`reports/ANALYSIS_MODELING_REPORT.md` 中的真实方法。
- 数据型图表不得在本工具重复生成。
- 论文阶段引用的非数据图都应有 `.drawio` 源文件和 PDF，或者在 `reports/DRAWIO_REPORT.md` 说明导出失败。
