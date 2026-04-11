# Changelog

## Unreleased (v0.6)

**New features**
- Stacked/dodged bar grouping: `.bar("x", "y", color="category")` now groups bars by category (dodged by default). Set `stacked=True` to stack bars instead.

**Bug fixes**
- DataAdapter now detects pandas and polars DataFrames even when the module-level import fails, using `type(data).__module__` as a fallback. Fixes a bug where `cerno.chart(df)` raised `TypeError: Unsupported data type: DataFrame` in certain environment configurations (e.g., Jupyter notebooks with separate venvs).

**Documentation**
- Pair plot moved from "Chart types" to "Layout" section in README and Sphinx docs, since `cerno.pairplot()` returns a `Grid`, not a `Chart`.

**Testing**
- 326 tests passing

---

## Unreleased (v0.5)

**New chart types**
- Countplot: `.countplot("x")` — bar chart of value counts, with optional categorical color grouping for side-by-side bars.
- ECDF: `.ecdf("x")` — empirical cumulative distribution function, with optional categorical color grouping.
- Rug plot: `.rug("x")` — tick marks along an axis, with configurable height and alpha. Useful as a layer on histograms or KDE plots.

**New features**
- Categorical color on box/violin: `.boxplot("x", "y", color="category")` and `.violin("x", "y", color="category")` now group by a third variable.
- Error bars: `.scatter()`, `.line()`, and `.bar()` accept `y_error` and `x_error` parameters (column name or array).
- Reference lines and bands: `.hline()`, `.vline()`, `.hband()`, `.vband()` for adding reference markers with optional labels and styling.
- Color palette API: `.palette("colorblind")` or `.palette(["#e63946", "#457b9d"])` to set named or custom palettes per chart. Built-in palettes: `cerno`, `pastel`, `bold`, `colorblind`.

**Testing**
- 319 tests passing

---

## Unreleased (v0.4)

**New chart types**
- KDE (kernel density estimation): `.kde("x")` — standalone density plot with optional fill, categorical color grouping, configurable bandwidth. Requires scipy.
- Strip plot: `.strip("x", "y")` — individual data points with random jitter along a categorical axis. Supports horizontal mode and wide-form data.
- Swarm plot: `.swarm("x", "y")` — beeswarm layout that avoids overlapping points along a categorical axis. Requires scipy.

**New features**
- Regression overlay: pass `fit=cerno.regression()` to `.scatter()` for linear or polynomial fit lines. Supports custom degree, color, linestyle, linewidth, and label. Uses numpy only (no scipy required).
- KDE histogram overlay: pass `kde=cerno.kde()` to `.histogram()` to overlay a density curve scaled to the histogram's y-axis.
- scipy optional dependency: `pip install cerno[scipy]` for KDE and swarm plot support.

**Internal improvements**
- Config object pattern: `Regression` and `KDE` are frozen dataclasses passed as parameters to existing marks, following the same pattern as `Grid`.
- `Layer.__post_init__` filters None values from encodings so `enc.get("key", default)` works correctly.
- Shared `render_categorical_scatter()` helper in `_base.py` eliminates duplication between strip and swarm renderers via pluggable `offset_fn` callback.
- `resolve_color_list()` utility added to `_base.py` for categorical scatter color resolution.
- KDE mark uses `dataclasses.replace()` for immutable config handling.
- `cerno/stats/` module added with `__init__.py` (scipy guard), `regression.py`, and `kde.py`.

**Testing**
- 282 tests passing

---

## Unreleased (v0.3)

**New features**
- Pair plot: `cerno.pairplot(df)` generates an NxN grid of scatter plots (off-diagonal) and histograms (diagonal) for all numeric columns. Supports `color` for categorical grouping and `columns` to select a subset. Returns a `Grid`.

**Bug fixes**
- Histogram now handles categorical color encoding by grouping (previously passed raw category names to matplotlib as color values, causing a crash)

**Internal improvements**
- `DataAdapter.column_names()` method added for listing available columns

**Testing**
- 245 tests passing

---

## v0.2

**New chart types**
- Box plot: `.boxplot("x", "y")` — grouped boxes, horizontal mode, wide-form support
- Violin plot: `.violin("x", "y")` — distribution shapes, horizontal mode, wide-form support
- Heatmap: `.heatmap()` — matrix form (DataFrame is the matrix) and long-form (x, y, color columns pivoted internally). Custom colormaps and cell annotations.
- Area chart: `.area("x", "y")` — filled area, stacked area from wide-form data, categorical color grouping

**New features**
- Polars support: pass a Polars DataFrame to `cerno.chart()` and use it exactly like pandas. Install with `pip install cerno[polars]`.
- Two-variable faceting: `.facet("col_var", row="row_var")` creates a row × column grid of subplots. Row-only faceting with `.facet(row="var")`.
- pandas is now an optional dependency — install with `pip install cerno[pandas]`. Core cerno works with dicts, numpy arrays, and lists.

**Breaking changes**
- `Grid` is now a standalone class in `cerno/layout/grid.py`, no longer part of `Chart`. `cerno.grid(2, 2)` returns a `Grid` instance (not a `Chart`). The `chart().grid(...)` pattern no longer works.

**Previously shipped features (v0.1 cycle)**
- Faceting: `cerno.chart(df).scatter("x", "y").facet("category")` splits data by a categorical column into subplots. Chart-level `.title()` becomes a super-title; each panel is titled with its category value. Panels wrap after `cols` columns (default 3).
- Wide-form scatter: `.scatter("x", ["col_a", "col_b"])` renders one series per column with automatic colors and legend labels
- Wide-form bar: `.bar("x", ["col_a", "col_b"])` renders grouped bars with automatic offset positioning, colors, and legend labels. Supports `horizontal=True`.
- Input validation module (`cerno/core/validate.py`) with plain-English error messages for: array length mismatches, non-numeric histogram data, NaN/Inf warnings, and invalid stroke dash styles
- `DataAdapter.subset(mask)` returns a filtered adapter for row-level subsetting (used by faceting)
- `Grid` supports `.title()`, `.theme()`, `.apply()`, `.show()`, `.save()`
- Grid-level `.apply(func)` receives `(figure, axes_2d_array)` for full matplotlib access
- Empty grid cells are automatically hidden
- Dark theme (`cerno_dark`) now includes a high-contrast color cycle

**Bug fixes**
- Violin wide-form now correctly applies user color encoding (previously silently ignored)
- Figure memory leak: `.save()` now closes the figure after writing (both single charts and grids)
- `default_colors()` now uses `CERNO_PALETTE.categorical` instead of matplotlib's tab10, so categorical colors are consistent with the active theme
- Grid figures now created inside theme context (previously ignored theme)
- `_normalize_size()` always returns numpy arrays (previously mixed list/array return types)
- `_normalize_size()` equal-value fallback now uses midpoint of min/max size instead of hardcoded 100
- Size encoding in scatter now raises on resolution failure instead of silently swallowing the error
- Size encoding in scatter categorical path resolved once instead of N times per category

**Internal improvements**
- `DataAdapter` exposes `raw_data` and `data_type` properties — marks use these instead of private `_data`/`_type` attributes
- Box plot and violin renderers now validate array lengths with `check_array_lengths()`
- PEP 8 cleanup: long guard condition in `iter_color_groups` broken across lines, extra blank lines removed in `validate.py`, misaligned indentation fixed in `facet.py`
- `Grid` extracted from `Chart` into dedicated `cerno/layout/grid.py` class
- `Chart._render_onto(figure, axes, adapter=None)` added so `Grid` and faceting render panels without reaching into Chart internals
- Redundant validation removed: `check_alpha`, `check_limit_order`, `check_positive_dimensions`, `check_scale`, `check_ticks_labels`, `check_xy_tuple` — matplotlib provides equally clear errors for these
- Shared wide-form utilities extracted to `_base.py`: `is_wide_form()`, `render_wide_form()`
- Shared distribution mark helper `group_by_x()` in `_base.py`
- `DataAdapter._detect_type` uses `isinstance(data, pd.DataFrame)` instead of string comparison
- `apply_color()` no longer returns a value — consistent with `apply_label()`
- Dark theme colors extracted to `_CERNO_DARK_PALETTE` constant
- All imports moved to top of file per PEP 8 (no more lazy imports in methods)
- `layout/__init__.py` simplified to docstring only, breaking circular import chain
- `Palette` dataclass uses `list[str]` instead of `typing.List[str]`
- Dead stubs removed: `data/transform.py`, `Chart._facet_opts`
- `DataAdapter` created once per `_render()` call, not per layer
- `render_layer()` accepts adapter directly instead of raw data
- Shared mark helpers extracted to `_base.py`: `apply_label()`, `apply_color()`, `iter_color_groups()`
- `Canvas.from_existing()` classmethod replaces direct private attribute access
- Redundant `_built` flag removed from Canvas
- `check_stroke_dash` uses `_DASH_STYLES` as single source of truth
- `warn_nan_inf` uses `np.isfinite().all()` fast path for clean data
- Sphinx theme switched from Furo to PyData Sphinx Theme

**Testing**
- 229 tests covering data layer, core API, all mark types (including wide-form and distribution), theming, grid layout, single- and two-variable faceting, Polars integration, and input validation

---

## v0.1.0

Initial release.

**Chart types**
- Scatter: color encoding (categorical and numeric), size encoding, alpha
- Line: single series, wide-form multi-series, long-form color grouping, stroke dash styles
- Bar: vertical and horizontal, color encoding
- Histogram: configurable bins, works with raw arrays

**Theming**
- Three built-in themes: `cerno_modern`, `cerno_dark`, `cerno_print`
- Global theme via `cerno.set_theme()`
- Per-chart theme via `.theme()`
- Scoped theme via `cerno.theme_context()`
- Custom theme creation via `Theme.merge()` and `cerno.register_theme()`

**Layout**
- `cerno.grid(rows, cols)` multi-panel layout

**Data formats**
- pandas DataFrame (long-form and wide-form)
- Python dict
- numpy arrays and Python lists

**Escape hatch**
- `.apply(func)` for direct matplotlib access

**Bug fixes**
- `is_categorical()` no longer crashes on empty arrays
- `_normalize_size()` handles empty arrays gracefully
- `cerno.grid(1, 1)` no longer crashes (scalar Axes from `plt.subplots` now handled)
- Color resolution with `data=None` and a literal color string no longer raises `ValueError`

**Internal improvements**
- Shared mark utilities (`resolve_color`, `default_colors`) extracted to `marks/_base.py`, eliminating code duplication across all four mark renderers
- `Chart._apply_decorators` refactored into table-driven setters and focused private methods
- `DataAdapter._resolve_column` consolidated duplicate branches
- Color palette defined in a single source of truth (`style/color.py`)

**Testing**
- Added pytest test suite with 138 tests covering data layer, core chart API, all mark types, theming, and grid layout
