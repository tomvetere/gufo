# Changelog

## Unreleased

**Breaking changes**
- `Grid` is now a standalone class in `cerno/layout/grid.py`, no longer part of `Chart`. `cerno.grid(2, 2)` returns a `Grid` instance (not a `Chart`). The `chart().grid(...)` pattern no longer works.
- `Chart.facet()` method removed (was a no-op stub). Faceting will be re-added in v0.2 with a working implementation.

**New features**
- Input validation module (`cerno/core/validate.py`) with plain-English error messages for: array length mismatches, invalid alpha, swapped axis limits, invalid scale names, tick/label count mismatches, invalid annotate coordinates, non-numeric histogram data, and NaN/Inf warnings
- `Grid` supports `.title()`, `.theme()`, `.apply()`, `.show()`, `.save()`
- Grid-level `.apply(func)` receives `(figure, axes_2d_array)` for full matplotlib access
- Empty grid cells are automatically hidden
- Dark theme (`cerno_dark`) now includes a high-contrast color cycle

**Bug fixes**
- Figure memory leak: `.save()` now closes the figure after writing (both single charts and grids)
- `default_colors()` now uses `CERNO_PALETTE.categorical` instead of matplotlib's tab10, so categorical colors are consistent with the active theme
- Grid figures now created inside theme context (previously ignored theme)
- `_normalize_size()` always returns numpy arrays (previously mixed list/array return types)
- `_normalize_size()` equal-value fallback now uses midpoint of min/max size instead of hardcoded 100
- Size encoding in scatter now warns on resolution failure instead of silently ignoring
- Size encoding in scatter categorical path resolved once instead of N times per category

**Internal improvements**
- `Grid` extracted from `Chart` into dedicated `cerno/layout/grid.py` class
- `Chart._render_onto(figure, axes)` added so `Grid` renders panels without reaching into Chart internals
- `DataAdapter._detect_type` uses `isinstance(data, pd.DataFrame)` instead of string comparison
- `apply_color()` no longer returns a value — consistent with `apply_label()`
- Dark theme colors extracted to `_CERNO_DARK_PALETTE` constant
- All imports moved to top of file per PEP 8 (no more lazy imports in methods)
- `Palette` dataclass uses `list[str]` instead of `typing.List[str]`
- Dead stubs removed: `facet.py`, `data/transform.py`, `Chart._facet_opts`
- `DataAdapter` created once per `_render()` call, not per layer
- `render_layer()` accepts adapter directly instead of raw data
- Shared mark helpers extracted to `_base.py`: `apply_label()`, `apply_color()`, `iter_color_groups()`
- `Canvas.from_existing()` classmethod replaces direct private attribute access
- Redundant `_built` flag removed from Canvas
- `check_stroke_dash` uses `_DASH_STYLES` as single source of truth
- `check_scale` queries matplotlib's scale registry at runtime
- `warn_nan_inf` uses `np.isfinite().all()` fast path for clean data

**Testing**
- Test suite expanded from 138 to 191 tests
- New `test_validation.py` with 40 unit tests for all validation helpers
- Integration validation tests added to `test_core.py` and `test_marks.py`
- Layout tests rewritten for standalone `Grid` class

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
