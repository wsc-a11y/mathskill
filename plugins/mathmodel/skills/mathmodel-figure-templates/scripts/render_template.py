#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

# 补充 matplotlib 模板（seaborn 无对应图型的专业科研图）
SCRIPT_MAP = {
    "multiclass-shap-combo": "make_multiclass_shap_combo.py",
    "cv-roc-ci": "make_cv_roc_ci.py",
    "taylor-diagram": "make_taylor_diagram.py",
    "rf-tpe-surface": "make_rf_tpe_surface.py",
    "grouped-circular-heatmap": "make_grouped_circular_heatmap.py",
    "nature-chord-diagram": "make_nature_chord_diagram.py",
}

SKILL_ROOT = Path(__file__).resolve().parents[1]
SEABORN_EXAMPLES_DIR = SKILL_ROOT / "references" / "seaborn-examples"


def seaborn_templates() -> dict[str, Path]:
    """扫描 references/seaborn-examples/*.py，key 为文件名 stem（下划线形式）。"""
    if not SEABORN_EXAMPLES_DIR.exists():
        return {}
    return {p.stem: p for p in sorted(SEABORN_EXAMPLES_DIR.glob("*.py"))}


ALIASES = {
    "shap": "multiclass-shap-combo",
    "multiclass-shap": "multiclass-shap-combo",
    "roc": "cv-roc-ci",
    "cv-roc": "cv-roc-ci",
    "taylor": "taylor-diagram",
    "surface": "rf-tpe-surface",
    "tpe": "rf-tpe-surface",
    "circular-heatmap": "grouped-circular-heatmap",
    "chord": "nature-chord-diagram",
    "circos": "nature-chord-diagram",
}

# 中文提示词 → 模板 id，按插入顺序匹配，具体词放前面（如"环形热图"在"热图"前）
CJK_HINTS = {
    "环形热图": "grouped-circular-heatmap",
    "多分类": "multiclass-shap-combo",
    "shap": "multiclass-shap-combo",
    "roc": "cv-roc-ci",
    "泰勒": "taylor-diagram",
    "tpe": "rf-tpe-surface",
    "和弦": "nature-chord-diagram",
    "circos": "nature-chord-diagram",
    "逻辑回归": "sns-logistic-regression",
    "回归": "sns-multiple-regression",
    "残差": "sns-residplot",
    "山脊": "sns-kde-ridgeplot",
    "ridge": "sns-kde-ridgeplot",
    "相关": "sns-many-pairwise-correlations",
    "小提琴": "sns-grouped-violinplots",
    "箱线": "sns-grouped-boxplot",
    "柱状": "sns-grouped-barplot",
    "条形": "sns-grouped-barplot",
    "误差带": "sns-errorband-lineplots",
    "联合分布": "sns-joint-kde",
    "调色板": "sns-palette-choices",
    "ecdf": "sns-multiple-ecdf",
    "热图": "sns-spreadsheet-heatmap",
    "曲面": "rf-tpe-surface",
}


def normalize(value: str) -> str:
    value = value.strip().lower().replace("_", "-")
    value = re.sub(r"[^a-z0-9\-]+", "-", value)
    value = re.sub(r"-+", "-", value).strip("-")
    return value


def resolve_template(value: str) -> tuple[str, Path]:
    raw = value.strip()
    key = normalize(raw)
    if key in SCRIPT_MAP:
        return key, SKILL_ROOT / "scripts" / "templates" / SCRIPT_MAP[key]
    sns_map = seaborn_templates()
    if key.startswith("sns-"):
        stem = key[4:].replace("-", "_")
        if stem in sns_map:
            return key, sns_map[stem]
    if key in ALIASES:
        return resolve_template(ALIASES[key])
    lowered = raw.lower()
    for hint, template_id in CJK_HINTS.items():
        if hint.lower() in lowered:
            return resolve_template(template_id)
    raise SystemExit(
        f"Unknown template: {value}\nRun with --list to see all available ids."
    )


def render_seaborn_example(dst: Path, stem: str, outputs_dir: Path, project: Path) -> list[Path]:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import runpy

    sys.path.insert(0, str(dst.parent))
    try:
        runpy.run_path(str(dst), run_name="__main__")
    except SystemExit as exc:
        if exc.code not in (None, 0):
            raise
    except Exception:
        raise

    figs = [plt.figure(n) for n in plt.get_fignums()]
    if not figs:
        raise SystemExit(f"No figures were created by {dst.name}")
    outputs: list[Path] = []
    multi = len(figs) > 1
    for i, fig in enumerate(figs, start=1):
        suffix = f"_{i}" if multi else ""
        for ext in (".png", ".pdf", ".svg"):
            path = outputs_dir / f"{stem}_replica{suffix}{ext}"
            fig.savefig(path, bbox_inches="tight")
            outputs.append(path)
    return outputs


def write_readme(project: Path, template_id: str, script_path: Path, output_paths: list[Path]) -> None:
    readme = project / "README.md"
    outputs_block = "\n".join(f"- `{p.as_posix()}`" for p in output_paths)
    block = f"""
## {template_id}

Generated from the bundled MathModel figure-template skill.

```bash
python3 {script_path.as_posix()}
```

Outputs:

{outputs_block}
""".strip()
    if readme.exists():
        text = readme.read_text(encoding="utf-8")
        marker = f"## {template_id}"
        if marker in text:
            return
        readme.write_text(text.rstrip() + "\n\n" + block + "\n", encoding="utf-8")
    else:
        readme.write_text("# 绘图复刻\n\n" + block + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Render a bundled MathModel figure template.")
    parser.add_argument("template", nargs="?", help="Template id, alias, or Chinese title fragment")
    parser.add_argument("--project", default="绘图复刻", help="Output project directory, default: 绘图复刻")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite an existing copied workspace script")
    parser.add_argument("--list", action="store_true", help="List supported template ids")
    args = parser.parse_args()

    if args.list:
        sns_map = seaborn_templates()
        print(f"seaborn 官方模板（{len(sns_map)}）:")
        for stem in sns_map:
            print(f"  sns-{normalize(stem)}")
        print(f"补充模板（{len(SCRIPT_MAP)}）:")
        for template_id in sorted(SCRIPT_MAP):
            print(f"  {template_id}")
        return
    if not args.template:
        parser.error("template is required unless --list is used")

    template_id, src = resolve_template(args.template)
    if not src.exists():
        raise SystemExit(f"Bundled script missing: {src}")

    project = Path(args.project).expanduser().resolve()
    scripts_dir = project / "scripts"
    outputs_dir = project / "outputs"
    scripts_dir.mkdir(parents=True, exist_ok=True)
    outputs_dir.mkdir(parents=True, exist_ok=True)

    dst = scripts_dir / src.name
    if dst.exists() and not args.overwrite:
        print(f"Using existing workspace script: {dst}")
    else:
        shutil.copy2(src, dst)
        print(f"Copied template script: {dst}")

    stem = dst.stem.removeprefix("make_")
    if template_id.startswith("sns-"):
        # seaborn 官方示例自带数据且不含 savefig（面向 sphinx-gallery），
        # 在渲染器进程内执行并用 Agg 收集所有 figure 保存，不修改官方代码。
        output_paths = render_seaborn_example(dst, stem, outputs_dir, project)
    else:
        result = subprocess.run([sys.executable, str(dst)], cwd=str(project), check=False)
        if result.returncode != 0:
            raise SystemExit(result.returncode)
        output_paths = [outputs_dir / f"{stem}_replica{suffix}" for suffix in (".png", ".pdf", ".svg")]

    write_readme(project, template_id, dst, output_paths)
    for path in output_paths:
        print(path)


if __name__ == "__main__":
    main()
