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
│   └── canvas.py        # matplotlib figure/axes lifecycle
├── marks/
│   ├── __init__.py      # render_layer() dispatcher
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
│   └── color.py         # Palette dataclass
└── layout/
    ├── grid.py          # Grid(rows, cols) — multi-panel layout
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
2. `Canvas.build()` creates fig/axes
3. Each `Layer` dispatched via `render_layer(layer, data, axes)`
4. `_apply_decorators()` sets titles, labels, axis options, legend
5. Each `.apply()` function called as `func(figure, axes)`

## What the README is

`README.md` is the API spec. All public-facing behavior should be derivable from it. If a feature isn't in the README, it isn't part of the public API.

## Dependencies

- `matplotlib >= 3.5.0`
- `pandas >= 1.3.0`
- `numpy >= 1.21.0`
- Python `>= 3.9`

Polars is planned for v0.2 as an optional dependency.

## Roadmap

- **v0.1**: scatter, line, bar, histogram, theming, wide-form data, grid layout
- **v0.2**: box, heatmap, area, violin, polars support, faceting
- **v0.3**: regression overlay, pair plot, interactive/Plotly backend
