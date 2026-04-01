# Changelog

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
