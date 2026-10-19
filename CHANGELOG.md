# Changelog

All notable changes to gufo are recorded here.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and from v0.1.0 onward this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html). See the [release policy](CLAUDE.md#release-policy) in `CLAUDE.md` for the rules governing breaking changes and deprecations.

Entries through v0.0.9 were reconstructed from the project roadmap and pre-date tagged releases, so dates on those entries are approximate. For the full per-version detail (internal refactors, test counts, etc.) see [`docs/changelog.md`](docs/changelog.md).

## [Unreleased]

## [0.2.2] — 2026-10-18

### Fixed
- **Wide-form bar charts honour `order=`.** `.bar("x", ["a", "b"], order=[...])` ignored `order=` and drew every row in data order. Error bars now follow `order=` too: `y_error=`/`x_error=` were taken from the original rows, so they landed on the wrong bars or raised a shape mismatch when `order=` dropped a category. Bar `x`/`y` and error lengths are checked before reordering, so an array longer than `x` raises instead of being silently truncated.
- **A list or tuple `color=` now groups like an array.** A plain Python list or tuple drew nothing at all, though the legend still listed every group. This affected every mark that groups by colour.
- **Boolean columns are treated as categorical.** `scatter(color=<bool column>)` drew a gradient colorbar with no legend, and `bar(color=<bool column>)` crashed. Both now behave like any categorical column: one colour per value, labelled by `.legend()`. Faceting by a boolean column works. `pairplot()` no longer picks boolean or datetime columns, which its diagonal histogram then rejected.
- **Grouped violins draw cells that have one value.** A violin with `color=` skipped every cell with fewer than two values, so data with one value per cell gave a blank chart with no legend. One-value cells now draw like they do on an ungrouped violin, and a cell that holds only NaN is skipped.
- **`pointplot()` omits NaN instead of losing the whole category.** One NaN in `y` made that category's mean NaN, so the category disappeared. NaN values are now dropped, with a warning. An `x`/`y` length mismatch raises gufo's length message instead of a raw `IndexError`.
- **Long-form `heatmap()` checks its column lengths.** Mismatched `x`/`y`/`color` lengths were silently truncated into a partial matrix. They now raise.
- `rug()` warns about NaN in `x`, like `scatter`, `histogram`, `line` and `ecdf`.
- **The `kde=` overlay on `.histogram()` now matches the bars.** The curve was scaled by the number of points times the first bar's width, which only fits a plain vertical histogram with even bins. It was about 600x too tall with `density=True`, wrongly sized with uneven `bins=`, drawn sideways with `horizontal=True`, and nearly invisible with a categorical `color=`, where it was also one pooled curve for every group. The curve is now scaled to the bars' own area, and a grouped histogram gets one curve per group in that group's colour.
- **Faceted charts draw the title, subtitle and caption once.** Each panel was rendered with the chart's own decorators, so a two-variable facet repeated `.title()` in every panel below the top row, and `.subtitle()`/`.caption()` were stacked once per panel at the same spot. The title is now only the super-title above the panels, as documented, and the subtitle and caption are drawn once for the figure.
- **`colorbar=False` on a faceted chart no longer gives each panel its own colour scale.** It skipped the shared scale along with the shared colorbar, so the same colour meant a different value in each panel. It now hides only the bar.

## [0.2.1] — 2026-07-18

### Fixed
- **Re-rendering a chart no longer double-draws.** `Canvas.build()` cached the figure it created, so every render after the first drew on top of the previous render's artists. Calling `.save()` twice on the same chart produced a wrong second image.
- **`.clear()` now clears rendered output.** Because of the caching above, marks removed by `.clear()` were still drawn in the next render — the "reusing charts" idiom documented in `README.md` did not work.
- **`.show()` no longer leaks figures.** `Chart.show()` and `Grid.show()` never closed their figure the way `.save()` does, so each call left one open. Reusing a chart in a loop grew memory without bound.
- Read the Docs installed no documentation dependencies. `.readthedocs.yaml` requested a `docs` pip extra, but v0.2.0 moved those dependencies to a PEP 735 dependency-group, which `extra_requirements` cannot resolve.

### Changed
- `.show()` closes its figure after displaying it, unless matplotlib is in interactive mode (`plt.ion()`, `%matplotlib widget`), where the window or widget is still live. Code that relied on the figure remaining current after `.show()` — for example calling `plt.savefig()` afterwards — should use `.save()` or the `.apply()` escape hatch instead.

---

## [0.2.0] — 2026-04-18

### Added
- **Category ordering**: `order=` parameter on `bar`, `boxplot`, `violin`, `countplot`, `pointplot`, `strip`, `swarm`, and `histogram` controls the display order of categories on the x-axis. Values not in the order list are excluded.
- **Color group ordering**: `color_order=` parameter on all marks that accept `color=` controls the rendering and legend order of color groups.
- **Histogram grouping modes**: `multiple=` parameter on `histogram` — `"layer"` (overlay, default), `"stack"` (cumulative bars), or `"dodge"` (side-by-side bars).
- **Step histogram**: `fill=False` on `histogram` draws outline-only step histograms. Works with both ungrouped and grouped (stack/dodge) modes.

### Changed
- Dev dependencies (`pytest`, `sphinx`, etc.) moved from `[project.optional-dependencies]` to PEP 735 `[dependency-groups]`. Local development now uses `uv sync` instead of `pip install -e ".[dev]"`.

---

## [0.1.2] — 2026-04-17

### Fixed
- Docstring escape for `**extra_kwargs` in `KDE.render()` now renders correctly in Sphinx

### Changed
- Updated project logo

---

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
