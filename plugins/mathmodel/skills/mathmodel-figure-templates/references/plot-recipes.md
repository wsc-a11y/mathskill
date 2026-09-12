# Plot Recipes

Use bundled scripts first. These notes are only for customization after a template has been copied into the workspace.

- SHAP composite: stacked horizontal mean-absolute importance bars plus class/model beeswarm strips and a feature-value colorbar.
- ROC with CI: fold curves interpolated to a shared FPR grid, mean curve, standard-deviation band, AUC mean ± sd legend, and diagonal baseline.
- Taylor diagram: polar coordinates with angle `arccos(correlation)` and radius as model standard deviation.
- 3D tuning surface: `mpl_toolkits.mplot3d`, smooth response surface, colorbar, and checked camera angle.
- Circular heatmap: polar bars, flipped outer labels, central legend, and ring-specific color scales.
- Chord diagram: outer `Wedge` sectors and translucent Bezier `PathPatch` ribbons.
