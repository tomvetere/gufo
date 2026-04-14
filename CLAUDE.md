# Cerno — Claude Context

## What this project is

Cerno is a Python data visualization library built on matplotlib. It targets researchers, data explorers, and business users who want good-looking charts without fighting their tools.

The core design philosophy:
- **Fluent method-chaining only.** `cerno.chart(data).scatter(...).title(...).show()`. There is no functional API alias — one pattern, always.
- **Wide-form and long-form data both work natively.** No `pd.melt()` required.
- **Always returns `Chart` or `Grid`.** Every factory function returns a `Chart` or `Grid`. Never a FacetGrid, never an Axes.
- **One escape hatch: `.apply(func)`.** `func(figure, axes)` drops down to matplotlib and stays in the chain. No `.ax`, no `.fig` properties on the public API.
- **Deferred rendering.** Marks register `Layer` objects on the `Chart`. Nothing is drawn until `.show()` or `.save()`.

## Module structure

```
cerno/
├── __init__.py          # public API only — explicit __all__
├── _version.py
├── core/
│   ├── chart.py         # Chart class — the only thing users interact with
│   ├── layer.py         # Layer dataclass (one per mark call)
│   ├── canvas.py        # matplotlib figure/axes lifecycle
│   └── validate.py      # input validation helpers (check_array_lengths, check_numeric, etc.)
├── marks/
│   ├── __init__.py      # render_layer() dispatcher
│   ├── _base.py         # shared mark utilities (resolve_color, default_colors, apply_label, apply_color, iter_color_groups, is_wide_form, render_wide_form, group_by_x, resolve_color_list, resolve_errors, is_continuous_color, resolve_color_range, render_categorical_scatter, set_category_ticks)
│   ├── scatter.py       # render(layer, adapter, axes)
│   ├── line.py
│   ├── bar.py
│   ├── boxplot.py
│   ├── violin.py
│   ├── heatmap.py
│   ├── area.py
│   ├── histogram.py
│   ├── kde.py           # standalone KDE density plot
│   ├── strip.py         # jittered categorical scatter
│   ├── swarm.py         # beeswarm non-overlapping categorical scatter
│   ├── countplot.py     # bar chart of value counts
│   ├── ecdf.py          # empirical cumulative distribution function
│   ├── rug.py           # tick marks along an axis
│   └── pointplot.py     # connected category means with CI
├── data/
│   ├── adapter.py       # DataAdapter.from_any() — resolves all input types to numpy
│   └── inference.py     # is_categorical()
├── style/
│   ├── theme.py         # Theme class, registry, set_theme, theme_context, built-in themes
│   └── color.py         # Palette dataclass, CERNO_PALETTE, NAMED_PALETTES, resolve_palette()
├── stats/
│   ├── __init__.py      # scipy guard (_require_scipy)
│   ├── regression.py    # Regression dataclass — fit overlay for scatter
│   ├── kde.py           # KDE dataclass — density estimation config
│   └── lowess.py        # Lowess dataclass — LOWESS smoothing overlay
└── layout/
    ├── grid.py          # Grid class — multi-panel layout container
    ├── facet.py         # render_facet() — split data by column into subplots
    ├── pairplot.py      # pairplot() — NxN scatter/histogram grid
    └── jointplot.py     # jointplot() — scatter with marginal distributions
```

## Style

Follow [PEP 8](https://peps.python.org/pep-0008/) and [PEP 20 (The Zen of Python)](https://peps.python.org/pep-0020/). In particular:
- Imports are always at the top of the file, never inside functions or methods.
- Import order: standard library, third-party, local — separated by blank lines.
- Beautiful is better than ugly. Simple is better than complex. Readability counts.
- Explicit is better than implicit. Errors should never pass silently.
- There should be one — and preferably only one — obvious way to do it.

## Key conventions

### Adding a new chart type

1. Create `cerno/marks/<type>.py` with a single `render(layer, adapter, axes)` function
2. Register it in `cerno/marks/__init__.py` under `_REGISTRY`
3. Add the method to `Chart` in `cerno/core/chart.py` — it appends a `Layer` and returns `self`
4. Document it in `README.md` with copy-pasteable examples

### Statistical overlays (regression, KDE)

Overlays are **config object classes** in `cerno/stats/`, passed as parameters to existing marks:
- `cerno.regression()` → `Regression` dataclass, passed via `fit=` on `.scatter()`
- `cerno.kde()` → `KDE` dataclass, passed via `kde=` on `.histogram()`, or used standalone via `.kde()`
- `cerno.lowess()` → `Lowess` dataclass, passed via `fit=` on `.scatter()`

Each config class has a `render()` method that draws itself onto axes. The mark renderer checks for the config object and delegates rendering. Factory functions in `cerno/__init__.py` create the config instances. This pattern avoids signature bloat and keeps overlay logic separate from mark logic.

### Data resolution

Marks never receive raw DataFrames. Always go through `DataAdapter.resolve(key)` which returns a numpy array. This is the only place where column name → array resolution happens. When a mark needs the raw data object (e.g. heatmap matrix form), use the public `adapter.raw_data` and `adapter.data_type` properties — never access `_data` or `_type` directly.

### Theme

Themes are immutable. `.merge(overrides)` returns a new `Theme`. Use `plt.rc_context()` via `theme.as_context()` to scope a theme — never call `plt.rcParams.update()` directly in mark code.

### Rendering pipeline (in `Chart._render()`)

1. Resolve theme → enter `theme.as_context()`
2. `Canvas.build()` creates fig/axes
3. Delegate to `_render_onto(fig, axes)`:
   a. Create `DataAdapter` once for the chart's data (not per layer)
   b. Resolve palette via `resolve_palette()`; stamp on each `Layer`
   c. Each `Layer` dispatched via `render_layer(layer, adapter, axes)`
   d. `_apply_decorators()` sets references, titles, labels, axis options, legend
   e. Each `.apply()` function called as `func(figure, axes)`

Grid rendering is handled by `Grid._render()` in `layout/grid.py`:
1. `plt.subplots(rows, cols)` inside theme context
2. Each panel rendered via `panel._render_onto(figure, axes)` — Grid never reaches into Chart internals
3. Panel-level theme overrides respected via nested context
4. Grid-level `.title()` → `fig.suptitle()`
5. Unassigned cells hidden
6. Grid-level `.apply()` functions called with `(fig, axes_2d_array)`

### Input validation

Validation lives in `core/validate.py` — small pure functions that raise `ValueError` or `warnings.warn`. Only checks that genuinely improve on matplotlib's own error messages belong here.

- **Render-time checks** (in mark renderers): array length mismatches (`check_array_lengths`), numeric type for histogram (`check_numeric`), NaN/Inf warnings (`warn_nan_inf`), stroke dash validation (`check_stroke_dash`). These require resolved data and fire during `_render()`.
- **Do not duplicate matplotlib.** If matplotlib already raises a clear error for invalid input (alpha out of range, bad scale name, negative figsize, etc.), do not add a cerno-level check. Only add validation when cerno can provide a meaningfully better message.

### Grid layout

Grid is a standalone layout container, separate from Chart. Usage:

```python
g = cerno.grid(2, 2, figsize=(14, 10))
g[0, 0] = cerno.chart(df).scatter("x", "y").title("Panel A")
g[0, 1] = cerno.chart(df).line("x", "y").title("Panel B")
g.show()
```

- `cerno.grid(rows, cols)` creates a `Grid` instance directly
- `Grid.__setitem__` stores panel Charts in `_panels`
- `Grid.__getitem__` raises `TypeError` (panels are write-only — no implicit state)
- `Grid._render()` creates subplots and delegates to each panel
- `Grid.title()`, `.theme()`, `.apply()`, `.show()`, `.save()` for grid-level options

### Testing

Run `python -m pytest tests/` after every change to verify correctness. All tests must pass before committing.

## What the README is

`README.md` is the API spec. All public-facing behavior should be derivable from it. If a feature isn't in the README, it isn't part of the public API.

## Dependencies

Core:
- `matplotlib >= 3.5.0`
- `numpy >= 1.21.0`
- Python `>= 3.10`

Optional extras:
- `cerno[pandas]` — `pandas >= 1.3.0`
- `cerno[polars]` — `polars >= 0.20.0`
- `cerno[scipy]` — `scipy >= 1.7.0` (required for KDE and swarm)
- `cerno[stats]` — `statsmodels >= 0.13.0` (required for LOWESS smoothing)
- `cerno[all]` — all optional dependencies

pandas, polars, scipy, and statsmodels are guarded with `try/except ImportError` at import time. If neither is installed, cerno still works with dicts, arrays, and lists. KDE and swarm raise `ImportError` with install instructions when scipy is missing. LOWESS raises `ImportError` when statsmodels is missing. Regression uses numpy only.

## Roadmap

- **v0.0.1**: scatter, line, bar, histogram, theming, wide-form data, grid layout, faceting, input validation
- **v0.0.2**: box, heatmap, area, violin, polars support, two-variable faceting — complete
- **v0.0.3**: pair plot — complete
- **v0.0.4**: regression overlay, KDE/density plot, strip/swarm plots (scipy optional dependency) — complete
- **v0.0.5**: categorical color on box/violin, countplot, error bars, rugplot, ECDF, color palette API, reference lines/bands — complete
- **v0.0.6**: stacked/dodged bar grouping, continuous color scales on scatter, jointplot, Grid ratios, horizontal histogram, docstrings, gallery, tutorial — complete
- **v0.0.7**: data labels, pointplot, LOWESS smoothing, facet sharex/sharey, legend outside — complete
- **v0.0.8**: shared colorbar/legend on faceted charts, continuous color on line, `.label()` on line and pointplot, error bands on area — complete
- **v0.1.0**: target first tagged release
