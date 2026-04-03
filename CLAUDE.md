# Cerno — Claude Context

## What this project is

Cerno is a Python data visualization library built on matplotlib. It targets researchers, data explorers, and business users who want good-looking charts without fighting their tools.

The core design philosophy:
- **Fluent method-chaining only.** `cerno.chart(data).scatter(...).title(...).show()`. There is no functional API alias — one pattern, always.
- **Wide-form and long-form data both work natively.** No `pd.melt()` required.
- **Always returns `Chart`.** Every factory function and layout method returns a `Chart`. Never a FacetGrid, never an Axes.
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
│   └── validate.py      # input validation helpers (check_alpha, check_array_lengths, etc.)
├── marks/
│   ├── __init__.py      # render_layer() dispatcher
│   ├── _base.py         # shared mark utilities (resolve_color, default_colors, apply_label, apply_color, iter_color_groups)
│   ├── scatter.py       # render(layer, adapter, axes)
│   ├── line.py
│   ├── bar.py
│   └── histogram.py
├── data/
│   ├── adapter.py       # DataAdapter.from_any() — resolves all input types to numpy
│   ├── inference.py     # is_categorical(), is_datetime()
│   └── transform.py     # (future) aggregations, binning
├── style/
│   ├── theme.py         # Theme class, registry, set_theme, theme_context
│   ├── defaults.py      # (future) built-in theme definitions
│   └── color.py         # Palette dataclass + CERNO_PALETTE
└── layout/
    └── facet.py         # (future) facet by data column
```

## Key conventions

### Adding a new chart type

1. Create `cerno/marks/<type>.py` with a single `render(layer, adapter, axes)` function
2. Register it in `cerno/marks/__init__.py` under `_REGISTRY`
3. Add the method to `Chart` in `cerno/core/chart.py` — it appends a `Layer` and returns `self`
4. Document it in `README.md` with copy-pasteable examples

### Data resolution

Marks never receive raw DataFrames. Always go through `DataAdapter.resolve(key)` which returns a numpy array. This is the only place where column name → array resolution happens.

### Theme

Themes are immutable. `.merge(overrides)` returns a new `Theme`. Use `plt.rc_context()` via `theme.as_context()` to scope a theme — never call `plt.rcParams.update()` directly in mark code.

### Rendering pipeline (in `Chart._render()`)

1. Resolve theme → enter `theme.as_context()`
2. Create `DataAdapter` once for the chart's data (not per layer)
3. `Canvas.build()` creates fig/axes
4. Each `Layer` dispatched via `render_layer(layer, adapter, axes)`
5. `_apply_decorators()` sets titles, labels, axis options, legend
6. Each `.apply()` function called as `func(figure, axes)`

For grid charts (`_grid_spec is not None`), `_render_grid()` takes over:
1. `plt.subplots(rows, cols)` inside theme context
2. Each panel Chart's layers rendered onto its grid cell axes
3. Panel-level theme overrides respected via nested context
4. Grid-level `.title()` → `fig.suptitle()`
5. Unassigned cells hidden

### Input validation

Validation lives in `core/validate.py` — small pure functions that raise `ValueError` or `warnings.warn`.

- **Call-time checks** (in `chart.py`): alpha, xlim/ylim order, scale names, tick/label length, annotate xy, figure dimensions. These fire immediately when the method is called.
- **Render-time checks** (in mark renderers): array length mismatches, numeric type (histogram), NaN/Inf warnings. These require resolved data and fire during `_render()`.

### Grid layout

Grid is part of Chart, not a separate class. Usage:

```python
g = cerno.chart().grid(2, 2, figsize=(14, 10))
g[0, 0] = cerno.chart(df).scatter("x", "y").title("Panel A")
g[0, 1] = cerno.chart(df).line("x", "y").title("Panel B")
g.show()
```

- `Chart.grid(rows, cols)` sets `_grid_spec`, returns self
- `Chart.__setitem__` stores panel Charts in `_grid_panels`
- `Chart.__getitem__` raises `TypeError` (panels are write-only — no implicit state)
- `Chart._render_grid()` creates subplots and delegates to each panel

## What the README is

`README.md` is the API spec. All public-facing behavior should be derivable from it. If a feature isn't in the README, it isn't part of the public API.

## Dependencies

- `matplotlib >= 3.5.0`
- `pandas >= 1.3.0`
- `numpy >= 1.21.0`
- Python `>= 3.9`

Polars is planned for v0.2 as an optional dependency.

## Roadmap

- **v0.1**: scatter, line, bar, histogram, theming, wide-form data, grid layout, input validation
- **v0.2**: box, heatmap, area, violin, polars support, faceting
- **v0.3**: regression overlay, pair plot, interactive/Plotly backend
