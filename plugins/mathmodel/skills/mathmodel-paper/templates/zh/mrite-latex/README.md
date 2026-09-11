# mrite-latex 模板（国赛样式 · 思源宋体）

> 来源：Mrite-Skills 项目（MIT），并入 mathskill 插件。format.cls 基于 cumcmthesis 改造，已禁用承诺书/编号页（`withoutpreface`），正文使用思源宋体。

## 文件清单

| 文件 | 说明 |
| --- | --- |
| `main.tex` | 主文件（原 `论文.tex` 改名，与模板族命名一致） |
| `format.cls` | 样式文件（页面 25mm 边距、1.38 倍行距、中文标题格式） |
| `fonts/` | 思源宋体（Bold + Regular），format.cls 通过 `Path = ./fonts/` 加载 |
| `0.摘要.tex` ~ `10.附录.tex` | 14 个带注释指导的空白章节模板 |

## 章节结构

```
0.摘要.tex                  # ≤900字，严格1页
1.引言.tex                  # 问题背景 + 问题重述
2.总体分析.tex              # 三段式逐问串联
3.模型假设.tex              # itemize，每条带编号
4.符号说明.tex              # 统一 longtable 表格
5.模型的建立与求解.tex      # 主文件，\input 各问题子文件
5.1.问题1的建立求解.tex     # 每问主文件，\input 两个子文件
5.1.1.分析与准备.tex        # 具体分析 + 流程图 + 模型准备
5.1.2.建模与求解.tex        # 模型建立 + 模型求解
6.模型检验.tex              # 误差分析 + 灵敏度分析
7.模型评价.tex              # 优点4条 + 缺点2条
8.模型改进推广.tex          # 各一段自然段落
9.参考文献.tex              # GB/T 7714-2015，8-15条
10.附录.tex                 # 附件说明表
```

多问题扩展：在 `5.模型的建立与求解.tex` 中按注释新增 `\input{5.2.问题2的建立求解.tex}` 等。

## 排版规范（此模板专属）

- **摘要**：≤900 字，严格 1 页；开头段 2 句 + 逐问摘要 + 结尾段 2 句
- **正文**：禁止分点符号（1. 2. 3.）；禁止加粗（摘要和问题重述除外）
- **图**：宽 `0.8\textwidth`；**表**：宽 `\textwidth`，统一 `longtable` 样式
- **参考文献**：GB/T 7714-2015 格式，8-15 条
- **表格行距**：tabular 环境已全局设为 1.38 倍行距（format.cls 内实现）
- **章节标题**：一级标题中文数字（一、二、…），居中

## 编译

```bash
xelatex -interaction=nonstopmode main.tex
xelatex -interaction=nonstopmode main.tex   # 跑两遍解决目录/交叉引用
```

依赖：xelatex + 完整 TeX 发行版宏包（ctex、mdframed、tikz、longtable、booktabs 等；MiKTeX/TeX Live 完整安装均可）。**必须用 xelatex**（格式类强制，pdflatex 会报错）。
