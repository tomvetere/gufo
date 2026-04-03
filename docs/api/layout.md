# Layout

Grid layout is part of the `Chart` class. See {py:class}`cerno.core.chart.Chart`.

Key methods:

- `Chart.grid(rows, cols, figsize=None)` — configure as a multi-panel grid
- `Chart.__setitem__(idx, panel_chart)` — assign a `Chart` to a grid cell
- `cerno.grid(rows, cols, figsize=None)` — convenience for `cerno.chart().grid(...)`
