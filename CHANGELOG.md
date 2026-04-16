# Changelog

All notable changes to gufo are recorded here.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and from v0.1.0 onward this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html). See the [release policy](CLAUDE.md#release-policy) in `CLAUDE.md` for the rules governing breaking changes and deprecations.

Entries through v0.0.9 were reconstructed from the project roadmap and pre-date tagged releases, so dates on those entries are approximate. For the full per-version detail (internal refactors, test counts, etc.) see [`docs/changelog.md`](docs/changelog.md).

## [0.1.1] — 2026-04-16

### Fixed
- Rendering no longer mutates stored `Layer` objects (uses `dataclasses.replace`)
- Facet columns containing `NaN` now warn and exclude `NaN` rows instead of producing invisible panels
- `kdeplot()` now passes `**kwargs` through to matplotlib
- Better error messages when arrays, lists, or Series are passed to `chart()` instead of a DataFrame/dict

### Changed
- `[test]` and `[dev]` extras added to `pyproject.toml`
- CI uses `pip install -e ".[test]"` instead of manual pytest install

---

## [0.1.0] — 2026-04-14

First tagged release.

### Added
- `density=` named parameter on `.histogram()`; previously only reachable via untyped `**kwargs` passthrough.
- `Chart.clear()` method — resets layers, titles, labels, annotations, and reference lines while keeping the bound data, theme, palette, figure size, and facet configuration. Returns `self` so it stays in the chain.
- "Building a chart" and "Reusing charts" sections in the README covering the three equivalent construction patterns (`gufo.chart(df).x()`, assigned variable, `from gufo import chart`) and the layer-accumulation behavior of `Chart`.
- Release policy documented in `CLAUDE.md` covering semver rules, breaking-change documentation, and the N→N+2 deprecation cycle.

### Changed
- **Renamed `Chart.kde()` → `Chart.kdeplot()`.** Breaks the name collision with the `gufo.kde()` overlay config factory, matches the `-plot` suffix already used by `boxplot`/`countplot`/`pointplot`, and aligns with seaborn's `sns.kdeplot`.
- `Chart.kdeplot()` now accepts flat parameters (`linestyle`, `linewidth`, `alpha`, `n_points`) that were previously silently dropped. Before this fix, calls like `.kde("x", linewidth=3)` had no effect.
- `Grid` removed from `gufo.__all__` to match its "use the `gufo.grid()` factory" guidance. The class is still importable from `gufo.layout.grid` if needed.
- Histogram docs note that extra keyword arguments forward to `matplotlib.axes.Axes.hist`; the same passthrough applies to the other marks (`scatter` → `Axes.scatter`, `line` → `Axes.plot`, `bar` → `Axes.bar`, etc.).

### Deprecated
- _(none)_

### Removed
- _(none)_

### Fixed
- `Chart.kde()` (now `.kdeplot()`) no longer silently drops KDE configuration kwargs. See **Changed** above.

---

## [0.0.9]

Release-hygiene pass ahead of the first PyPI tag. Package rename from `cerno` → `gufo`, CI workflow added, PyPI trusted-publishing configured, Read the Docs deployment wired up. No user-facing feature changes.

## [0.0.8]

Shared colorbar and legend on faceted charts; continuous color on `.line()`; `.label()` on line and pointplot; error bands on area. Internal: facet rendering switched to `layout="constrained"`.

## [0.0.7]

Data labels via `.label()`; pointplot; LOWESS smoothing (`fit=gufo.lowess()`, requires statsmodels); facet `sharex`/`sharey`; legend outside positioning.

## [0.0.6]

Stacked/dodged bar grouping; continuous color scales on scatter with automatic colorbar; jointplot; Grid `width_ratios`/`height_ratios`; horizontal histogram; full public-method docstring pass; visual gallery; getting-started tutorial.

## [0.0.5]

Countplot, ECDF, rug plot; categorical color on box/violin; error bars on scatter/line/bar; reference lines and bands (`.hline()`, `.vline()`, `.hband()`, `.vband()`); color palette API (`.palette()`).

## [0.0.4]

KDE density plot (standalone and as histogram overlay); strip and swarm plots; regression overlay via `fit=gufo.regression()`. scipy introduced as an optional dependency.

## [0.0.3]

Pair plot (`gufo.pairplot(df)`); categorical color grouping in histograms.

## [0.0.2]

Box plot, violin plot, heatmap, area chart; polars support; two-variable faceting; pandas becomes optional. **Breaking:** `Grid` extracted from `Chart` into a standalone class — the old `chart().grid(...)` pattern no longer works; use `gufo.grid(2, 2)` instead.

## [0.0.1]

Initial release. Scatter, line, bar, histogram; three built-in themes; grid layout; faceting; wide-form data; input validation; `.apply()` escape hatch.
