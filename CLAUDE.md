# Gufo — Claude Context

## What this project is

Gufo is a Python data visualization library built on matplotlib. It targets researchers, data explorers, and business users who want good-looking charts without fighting their tools.

The core design philosophy:
- **Fluent method-chaining only.** `gufo.chart(data).scatter(...).title(...).show()`. There is no functional API alias — one pattern, always.
- **Wide-form and long-form data both work natively.** No `pd.melt()` required.
- **Always returns `Chart` or `Grid`.** Every factory function returns a `Chart` or `Grid`. Never a FacetGrid, never an Axes.
- **One escape hatch: `.apply(func)`.** `func(figure, axes)` drops down to matplotlib and stays in the chain. No `.ax`, no `.fig` properties on the public API.
- **Deferred rendering.** Marks register `Layer` objects on the `Chart`. Nothing is drawn until `.show()` or `.save()`.
- **A convenience layer, not a platform.** A feature belongs only if it removes real boilerplate (aggregation, CI bands, wide-form wrangling). If `.apply()` plus a few lines of matplotlib does it, it doesn't belong in gufo.
- **One user-facing `Chart`, kept thin.** No mark subclasses (`Scatter(Chart)` breaks chaining). Chart methods store config and return `self`; logic lives in the modules Chart delegates to. Growth goes into internal mixins, never a second public entry point.
- **No Dask or PySpark.** Implicitly calling `.compute()`/`.toPandas()` on distributed data is a footgun; users aggregate first and pass pandas/polars.

## Style

Follow [PEP 8](https://peps.python.org/pep-0008/) and [PEP 20 (The Zen of Python)](https://peps.python.org/pep-0020/). In particular:
- Imports are always at the top of the file, never inside functions or methods.
- Import order: standard library, third-party, local — separated by blank lines.
- Beautiful is better than ugly. Simple is better than complex. Readability counts.
- Explicit is better than implicit. Errors should never pass silently.
- There should be one — and preferably only one — obvious way to do it.

## Key conventions

### Adding a new chart type

1. Create `gufo/marks/<type>.py` with a single `render(layer, adapter, axes)` function
2. Register it in `gufo/marks/__init__.py` under `_REGISTRY`
3. Add the method to `Chart` in `gufo/core/chart.py` — it appends a `Layer` and returns `self`
4. Document it in `README.md` with copy-pasteable examples

### Statistical overlays (regression, KDE)

Overlays are **config object classes** in `gufo/stats/`, passed as parameters to existing marks:
- `gufo.regression()` → `Regression` dataclass, passed via `fit=` on `.scatter()`
- `gufo.kde()` → `KDE` dataclass, passed via `kde=` on `.histogram()` as an overlay. For a standalone density plot, use `Chart.kdeplot()` (a flat-param mark method, not the overlay factory).
- `gufo.lowess()` → `Lowess` dataclass, passed via `fit=` on `.scatter()`

Each config class has a `render()` method that draws itself onto axes. The mark renderer checks for the config object and delegates rendering. Factory functions in `gufo/__init__.py` create the config instances. This pattern avoids signature bloat and keeps overlay logic separate from mark logic.

### Data resolution

Marks never receive raw DataFrames. Always go through `DataAdapter.resolve(key)` which returns a numpy array. This is the only place where column name → array resolution happens. When a mark needs the raw data object (e.g. heatmap matrix form), use the public `adapter.raw_data` and `adapter.data_type` properties — never access `_data` or `_type` directly.

### Theme

Themes are immutable. `.merge(overrides)` returns a new `Theme`. Use `plt.rc_context()` via `theme.as_context()` to scope a theme — never call `plt.rcParams.update()` directly in mark code.

### Rendering pipeline (in `Chart._render()`)

1. Resolve theme → enter `theme.as_context()`
2. `Canvas.reset()` discards any previously built figure, then `Canvas.build()` creates fig/axes. The reset is what makes re-rendering a `Chart` produce a clean figure instead of drawing on top of the previous render.
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
- **Do not duplicate matplotlib.** If matplotlib already raises a clear error for invalid input (alpha out of range, bad scale name, negative figsize, etc.), do not add a gufo-level check. Only add validation when gufo can provide a meaningfully better message.

### Grid layout

Grid is a standalone layout container, separate from Chart. Usage:

```python
g = gufo.grid(2, 2, figsize=(14, 10))
g[0, 0] = gufo.chart(df).scatter("x", "y").title("Panel A")
g[0, 1] = gufo.chart(df).line("x", "y").title("Panel B")
g.show()
```

- `gufo.grid(rows, cols)` creates a `Grid` instance directly
- `Grid.__setitem__` stores panel Charts in `_panels`
- `Grid.__getitem__` raises `TypeError` (panels are write-only — no implicit state)
- `Grid._render()` creates subplots and delegates to each panel
- `Grid.title()`, `.theme()`, `.apply()`, `.show()`, `.save()` for grid-level options

### Testing

Run `python -m pytest tests/` after every change to verify correctness. All tests must pass before committing.

### Commit messages

Never include `Co-Authored-By: Claude`, `Authored by Claude`, or any similar attribution line in commit messages or PR descriptions.

## What the README is

`README.md` is the API spec. All public-facing behavior should be derivable from it. If a feature isn't in the README, it isn't part of the public API.

## Dependencies

Only matplotlib and numpy are hard dependencies (versions live in `pyproject.toml`). Never import pandas, polars, scipy, or statsmodels unconditionally — guard with `try/except ImportError`, and when a feature needs one, raise `ImportError` naming the extra to install (e.g. `pip install gufo[scipy]`).

## Roadmap

Planned versions: `ROADMAP.md`. Release history: `CHANGELOG.md`.

## Release policy

Gufo follows [Semantic Versioning](https://semver.org/): `MAJOR.MINOR.PATCH`.

- **PATCH** (`0.1.x`) — bug fixes, docs, internal refactors. No public API changes.
- **MINOR** (`0.x.0`) — new marks, new parameters, new config objects, new themes. Must be backwards-compatible: existing code keeps working unchanged.
- **MAJOR** (`x.0.0`) — breaking changes to the public API. Pre-1.0, breaking changes may also ship in MINOR bumps, but must still follow the deprecation process below.

The public API is whatever is re-exported from `gufo/__init__.py` plus every method on `Chart` and `Grid`. Anything under a leading underscore or not re-exported is internal and may change at any time.

### Breaking changes

A change is breaking if it removes, renames, or changes the meaning of any public API — method names, parameter names, parameter defaults that alter output, return types, or the shape of `Layer`/`Theme`/`Palette` dataclasses when user code constructs them directly.

When a breaking change ships:
1. Add a **`### Breaking changes`** subsection to that version's entry in `CHANGELOG.md` listing each break and the migration path.
2. Cross-reference it from the README if the break affects anything shown in README examples.

### Deprecation process

Never remove a public API in a single release. The process is:

1. **Deprecate** in version N: keep the old API working, but emit a `DeprecationWarning` pointing at the replacement. Mark it in the docstring with `.. deprecated:: N` and state the removal version.
2. **Remove** no earlier than version N+2 (or the next MAJOR, whichever comes later). This gives users at least one full release cycle to migrate.
3. List deprecations under **`### Deprecated`** in the `CHANGELOG.md` entry for the version that introduces the warning, and again under **`### Breaking changes`** in the version that removes it.

Use `warnings.warn(msg, DeprecationWarning, stacklevel=2)` so the warning points at the caller, not gufo internals.
