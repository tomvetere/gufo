<p align="center">
  <img src="https://raw.githubusercontent.com/tomvetere/gufo/main/docs/_static/gufo_logo.png" alt="Gufo logo" width="200">
</p>

# Gufo

**Data visualization simplified.**

*Gufo* (Italian: /ˈɡu.fo/, **GOO-foh**) — "owl."

A Python data visualization library built on matplotlib. Designed for researchers, data explorers, and anyone making charts for reports or presentations who wants results fast without fighting their tools.

```python
import gufo

(
    gufo.chart(df)
    .scatter("gdp_per_capita", "life_expectancy", color="continent", size="population")
    .title("GDP vs Life Expectancy")
    .xlabel("GDP per Capita (USD)")
    .ylabel("Life Expectancy (years)")
    .legend()
    .save("output.png")
)
```

---

## Installation

```bash
pip install gufo
```

See [`CHANGELOG.md`](CHANGELOG.md) for release notes.

---

## Core principles

- **One API, one pattern.** Everything goes through `gufo.chart(data)`. No switching between function styles depending on what you want to do.
- **Works with your data as-is.** Pass a pandas DataFrame, Polars DataFrame, a numpy array, a dict, or raw lists — gufo handles the shape without requiring you to reshape first.
- **Matplotlib when you need it.** Gufo covers the common cases cleanly. When you need something custom, `.apply()` drops you into matplotlib without starting over.
- **Modern defaults.** Charts look good without any configuration.

---

## Quick Start

```python
import gufo
import pandas as pd

df = pd.read_csv("gapminder.csv")

gufo.chart(df).scatter("gdp_per_capita", "life_expectancy").show()
```

Polars works the same way:

```python
import polars as pl

df = pl.read_csv("gapminder.csv")
gufo.chart(df).scatter("gdp_per_capita", "life_expectancy").show()
```

---

## Building a chart

There are three equivalent ways to build a chart. Pick whichever reads best:

```python
# 1. Inline fluent chain — best for single-cell, self-contained plots
gufo.chart(df).histogram("income").title("Incomes").show()

# 2. Assign the chart, then add marks — useful for notebooks where you
#    build a plot across cells, or when you want to add layers conditionally
c = gufo.chart(df)
c.histogram("income")
if show_density:
    c.histogram("income", density=True, color="red")
c.title("Incomes").show()

# 3. Shorter call sites via direct import
from gufo import chart
c = chart(df).histogram("income")
c.show()
```

All three produce identical output — `gufo.chart()` and `from gufo import chart` are the same factory, and method chaining vs. separate statements are interchangeable because every chart method returns `self`.

### Reusing charts

Gufo builds charts lazily: every mark and decorator call registers a layer on the `Chart`, and nothing is drawn until `.show()` or `.save()`. Calling `.show()` does **not** clear those layers — so reusing a `Chart` variable across cells accumulates them. This is intentional (it's how layering works, e.g. scatter + regression line on one plot), but it can surprise users who expect a fresh plot per call.

Two idioms work:

```python
# Preferred: one fluent chain per plot
gufo.chart(df).histogram("income").show()
gufo.chart(df).histogram("income", density=True).show()

# Or: reuse the variable and reset explicitly between plots
c = gufo.chart(df)
c.histogram("income").show()
c.clear().histogram("income", density=True).show()
```

`.clear()` resets layers, titles, labels, annotations, and reference lines, but **keeps** the bound data, theme, palette, figure size, and facet configuration — so it's "start a fresh plot from this data/theme," not "reset to defaults."

---

## Chart types

### Scatter

```python
gufo.chart(df).scatter("x", "y").show()

# Encode a third variable as color or size
gufo.chart(df).scatter("x", "y", color="category", size="population").show()

# Transparency for dense data
gufo.chart(df).scatter("x", "y", alpha=0.4).show()

# Multiple series from wide-form data — no pd.melt() needed
gufo.chart(df).scatter("x", ["series_a", "series_b"]).show()

# Error bars
gufo.chart(df).scatter("x", "y", y_error="y_std").show()
gufo.chart(df).scatter("x", "y", y_error="y_std", x_error="x_std").show()
```

### Line

```python
gufo.chart(df).line("year", "revenue").show()

# Multiple series from wide-form data — no pd.melt() needed
wide_df = pd.DataFrame({
    "year":      [2020, 2021, 2022, 2023],
    "product_a": [100,  130,  160,  210],
    "product_b": [80,   95,   115,  140],
    "product_c": [60,   70,   90,   125],
})
gufo.chart(wide_df).line("year", ["product_a", "product_b", "product_c"]).show()

# Multiple series from long-form data
gufo.chart(long_df).line("year", "revenue", color="product").show()

# Dashed line style
gufo.chart(df).line("year", "forecast", stroke_dash="dashed").show()

# Error bars / confidence band
gufo.chart(df).line("year", "revenue", y_error="revenue_std").show()

# Gradient line colored by a numeric variable (with automatic colorbar)
gufo.chart(df).line("x", "y", color="speed", cmap="viridis").show()
```

### Bar

```python
gufo.chart(df).bar("region", "sales").show()

# Horizontal
gufo.chart(df).bar("region", "sales", horizontal=True).show()

# Colored by category
gufo.chart(df).bar("region", "sales", color="region").show()

# Grouped (dodged) bars by category
gufo.chart(df).bar("quarter", "revenue", color="region").legend().show()

# Stacked bars
gufo.chart(df).bar("quarter", "revenue", color="region", stacked=True).legend().show()

# Grouped bars from wide-form data
gufo.chart(df).bar("quarter", ["product_a", "product_b"]).show()

# Grouped bars, horizontal
gufo.chart(df).bar("quarter", ["product_a", "product_b"], horizontal=True).show()

# Error bars
gufo.chart(df).bar("region", "sales", y_error="sales_std").show()
```

### Histogram

```python
gufo.chart(df).histogram("income").show()

# Custom bin count
gufo.chart(df).histogram("income", bins=40).show()

# Normalized (area sums to 1)
gufo.chart(df).histogram("income", density=True).show()

# From a raw array
import numpy as np
data = np.random.normal(0, 1, 1000)
gufo.chart().histogram(data).show()

# With a KDE overlay (requires scipy)
gufo.chart(df).histogram("income", kde=gufo.kde()).show()

# Filled KDE overlay
gufo.chart(df).histogram("income", kde=gufo.kde(fill=True, alpha=0.3)).show()

# Step (outline-only) histogram
gufo.chart(df).histogram("income", fill=False).show()

# Grouped histograms: overlay (default), stack, or dodge
gufo.chart(df).histogram("income", color="region", multiple="layer").show()
gufo.chart(df).histogram("income", color="region", multiple="stack").show()
gufo.chart(df).histogram("income", color="region", multiple="dodge").show()
```

Any extra keyword arguments are forwarded to `matplotlib.axes.Axes.hist`, so options like `cumulative=True` work out of the box. The same passthrough applies to the other marks (`scatter` → `Axes.scatter`, `line` → `Axes.plot`, `bar` → `Axes.bar`, etc.).

### Box plot

```python
gufo.chart(df).boxplot("department", "salary").show()

# Horizontal
gufo.chart(df).boxplot("department", "salary", horizontal=True).show()

# Colored boxes
gufo.chart(df).boxplot("department", "salary", color="steelblue").show()

# Grouped by a categorical variable — side-by-side boxes
gufo.chart(df).boxplot("department", "salary", color="gender").legend().show()

# Multiple columns from wide-form data — each column becomes a box
gufo.chart(df).boxplot("x", ["q1_scores", "q2_scores", "q3_scores"]).show()
```

### Violin plot

```python
gufo.chart(df).violin("department", "salary").show()

# Horizontal
gufo.chart(df).violin("department", "salary", horizontal=True).show()

# Colored violins
gufo.chart(df).violin("department", "salary", color="steelblue").show()

# Grouped by a categorical variable — side-by-side violins
gufo.chart(df).violin("department", "salary", color="gender").legend().show()

# Multiple columns from wide-form data — each column becomes a violin
gufo.chart(df).violin("x", ["q1_scores", "q2_scores", "q3_scores"]).show()
```

### Heatmap

```python
# Matrix form — DataFrame is the heatmap
gufo.chart(pivot_df).heatmap().show()

# Long-form — pivoted internally
gufo.chart(df).heatmap("x_col", "y_col", color="value").show()

# Custom colormap and cell annotations
gufo.chart(pivot_df).heatmap(cmap="coolwarm", annotate=True).show()
```

### Area

```python
gufo.chart(df).area("x", "y").show()

# Stacked area from wide-form data
gufo.chart(df).area("x", ["series_a", "series_b"]).show()

# Colored area with transparency
gufo.chart(df).area("x", "y", color="steelblue", alpha=0.3).show()

# Grouped by category
gufo.chart(df).area("x", "y", color="category").show()

# Error band around the top edge
gufo.chart(df).area("x", "y", y_error="y_std").show()
```

### Regression overlay

```python
# Linear fit on a scatter plot
gufo.chart(df).scatter("x", "y", fit=gufo.regression()).show()

# Polynomial fit
gufo.chart(df).scatter("x", "y", fit=gufo.regression(degree=2)).show()

# Styled fit line
gufo.chart(df).scatter("x", "y", fit=gufo.regression(color="red", linestyle="--")).show()

# Regression with grouped scatter — one line fits all groups
gufo.chart(df).scatter("x", "y", color="category", fit=gufo.regression()).show()
```

### LOWESS smoothing

```python
# Non-parametric smooth on a scatter plot (requires statsmodels)
gufo.chart(df).scatter("x", "y", fit=gufo.lowess()).show()

# Custom smoothing fraction
gufo.chart(df).scatter("x", "y", fit=gufo.lowess(frac=0.3)).show()
```

### KDE (kernel density estimation)

```python
# Standalone density plot (requires scipy)
gufo.chart(df).kdeplot("x").show()

# Filled density
gufo.chart(df).kdeplot("x", fill=True).show()

# Grouped by category
gufo.chart(df).kdeplot("x", color="category").show()
```

### Strip plot

```python
# Jittered points along a categorical axis
gufo.chart(df).strip("department", "salary").show()

# Horizontal
gufo.chart(df).strip("department", "salary", horizontal=True).show()

# Custom jitter width and color
gufo.chart(df).strip("department", "salary", jitter=0.3, color="steelblue").show()

# Wide-form data
gufo.chart(df).strip(None, ["q1_scores", "q2_scores"]).show()
```

### Swarm plot

```python
# Non-overlapping points along a categorical axis (requires scipy)
gufo.chart(df).swarm("department", "salary").show()

# Horizontal
gufo.chart(df).swarm("department", "salary", horizontal=True).show()

# Colored
gufo.chart(df).swarm("department", "salary", color="coral").show()

# Wide-form data
gufo.chart(df).swarm(None, ["q1_scores", "q2_scores"]).show()
```

### Countplot

```python
# Bar chart of value counts
gufo.chart(df).countplot("department").show()

# Horizontal
gufo.chart(df).countplot("department", horizontal=True).show()

# Grouped by a second categorical variable
gufo.chart(df).countplot("department", color="gender").legend().show()
```

### ECDF

```python
# Empirical cumulative distribution function
gufo.chart(df).ecdf("income").show()

# Grouped by category
gufo.chart(df).ecdf("income", color="region").legend().show()
```

### Rugplot

```python
# Tick marks showing individual data points along the x axis
gufo.chart(df).rug("income").show()

# Commonly layered with a histogram or KDE
gufo.chart(df).histogram("income").rug("income").show()

# Custom height and transparency
gufo.chart(df).rug("income", height=0.1, alpha=0.8).show()

# Colored by category
gufo.chart(df).rug("income", color="region").legend().show()
```

### Point plot

```python
# Mean + 95% CI per category
gufo.chart(df).pointplot("day", "total_bill").show()

# Grouped by a second variable
gufo.chart(df).pointplot("day", "total_bill", color="gender").legend().show()
```

---

## Data labels

```python
# Label bars with their values
gufo.chart(df).bar("region", "sales").label().show()

# Custom formatting
gufo.chart(df).bar("region", "sales").label(fmt=".1f").show()

# Label scatter points with a column
gufo.chart(df).scatter("x", "y").label("name").show()

# Label each point on a line chart
gufo.chart(df).line("month", "revenue").label(fmt=".0f").show()

# Label pointplot means with a format string
gufo.chart(df).pointplot("day", "tip").label(fmt=".2f").show()
```

---

## Layering

Multiple marks can be added to the same chart. Each call registers a new layer rendered in order.

```python
(
    gufo.chart(df)
    .scatter("x", "y", alpha=0.5, label="Observations")
    .line("x", "trend", color="#333333", stroke_dash="dashed", label="Trend")
    .legend()
    .show()
)
```

---

## Reference lines and bands

```python
# Horizontal reference line
gufo.chart(df).scatter("x", "y").hline(50, label="Target").legend().show()

# Vertical reference line
gufo.chart(df).line("year", "revenue").vline(2020, color="red", label="Launch").legend().show()

# Horizontal band (shaded region)
gufo.chart(df).scatter("x", "y").hband(40, 60, color="green", alpha=0.1).show()

# Vertical band
gufo.chart(df).line("year", "gdp").vband(2008, 2009, label="Recession").show()

# Combine multiple references
(
    gufo.chart(df)
    .scatter("x", "y")
    .hline(50, label="Mean")
    .hband(40, 60, color="blue", alpha=0.1)
    .vline(3, color="red", linestyle=":")
    .legend()
    .show()
)
```

---

## Color palette

```python
# Set a named palette
gufo.chart(df).scatter("x", "y", color="category").palette("colorblind").show()

# Available named palettes: 'gufo' (default), 'pastel', 'bold', 'colorblind'

# Custom palette — pass a list of color strings
gufo.chart(df).bar("quarter", ["q1", "q2", "q3"]).palette(["#e63946", "#457b9d", "#2a9d8f"]).show()
```

---

## Labels and annotations

```python
(
    gufo.chart(df)
    .scatter("x", "y")
    .title("Chart Title")
    .subtitle("A clarifying subtitle shown below the title")
    .xlabel("Horizontal axis label")
    .ylabel("Vertical axis label")
    .caption("Source: World Bank, 2024")   # small text below the chart
    .show()
)

# Arrow annotation pointing to a specific data point
gufo.chart(df).scatter("x", "y").annotate("Outlier", xy=(42, 180)).show()
```

---

## Axis control

```python
(
    gufo.chart(df)
    .scatter("x", "y")
    .xlim(0, 100)
    .ylim(0, 500)
    .xscale("log")
    .xticks(rotation=45)
    .show()
)
```

---

## Category ordering

Control the display order of categories on the x-axis (`order=`) and color groups (`color_order=`). Values not in the order list are excluded from the plot.

```python
# Show only these departments, in this order
gufo.chart(df).boxplot("department", "salary", order=["Engineering", "Sales"]).show()

# Control color group order (affects legend and rendering order)
gufo.chart(df).scatter("x", "y", color="region", color_order=["West", "East"]).show()

# Works on bar, boxplot, violin, countplot, pointplot, strip, swarm, histogram
gufo.chart(df).countplot("category", order=["B", "A", "C"]).show()
```

`order=` is available on marks with a categorical x-axis. `color_order=` is available on all marks that accept `color=`.

---

## Legend

```python
# Basic legend
gufo.chart(df).scatter("x", "y", color="cat").legend().show()

# With title
gufo.chart(df).scatter("x", "y", color="cat").legend(title="Category").show()

# Positioned outside the axes
gufo.chart(df).scatter("x", "y", color="cat").legend(position="outside right").show()
gufo.chart(df).scatter("x", "y", color="cat").legend(position="outside bottom").show()

# Hidden
gufo.chart(df).scatter("x", "y", color="cat").legend(hide=True).show()
```

---

## Data input formats

Gufo accepts any of these without conversion:

```python
# Pandas DataFrame (long-form or wide-form)
gufo.chart(df).scatter("x", "y").show()

# Dict
gufo.chart({"x": [1, 2, 3], "y": [4, 5, 6]}).scatter("x", "y").show()

# Raw arrays or lists (no data argument needed)
gufo.chart().scatter([1, 2, 3], [4, 5, 6]).show()

import numpy as np
gufo.chart().line(np.arange(100), np.random.cumsum(np.random.randn(100))).show()
```

---

## Theming

```python
# Apply a theme globally (affects all subsequent charts)
gufo.set_theme("gufo_modern")   # default
gufo.set_theme("gufo_dark")
gufo.set_theme("gufo_print")    # black and white, print-safe

# Apply a theme to one chart only
gufo.chart(df).theme("gufo_dark").scatter("x", "y").show()

# Apply a theme temporarily with a context manager
with gufo.theme_context("gufo_print"):
    gufo.chart(df).scatter("x", "y").save("print_ready.pdf")

# Create and register a custom theme
my_theme = gufo.get_theme("gufo_modern").merge({
    "axes.facecolor": "#1a1a2e",
    "figure.facecolor": "#16213e",
}).rename("brand_dark")

gufo.register_theme(my_theme)
gufo.set_theme("brand_dark")
```

---

## Layout

### Multi-panel grid

```python
g = gufo.grid(rows=2, cols=2, figsize=(14, 10))

g[0, 0] = gufo.chart(df).scatter("x", "y").title("Panel A")
g[0, 1] = gufo.chart(df).line("year", "revenue").title("Panel B")
g[1, 0] = gufo.chart(df).histogram("income").title("Panel C")
g[1, 1] = gufo.chart(df2).bar("region", "sales").title("Panel D")

g.show()
```

`gufo.grid()` returns a `Grid`, a layout container for multiple charts. Assign
panels with `g[row, col] = gufo.chart(data).mark(...)`. Each panel is a normal
`Chart`, so all methods work as usual. Grid-level `.title()` becomes a super-title.

### Faceting by a data column

```python
# Split into one subplot per continent
gufo.chart(df).scatter("gdp", "life_exp").facet("continent").show()

# Control the number of columns before wrapping
gufo.chart(df).scatter("gdp", "life_exp").facet("continent", cols=4).show()

# Independent axes per panel (default is shared across all panels)
gufo.chart(df).scatter("gdp", "life_exp").facet("continent", sharex=False, sharey=False).show()
```

`facet()` takes a categorical column name and creates one panel per unique value,
each showing the same layers with only that subset of data. Chart-level `.title()`
becomes a super-title above all panels. Empty cells are hidden automatically.
`sharex` and `sharey` both default to `True`; set either to `False` for
independent per-panel scales.

When a faceted chart uses continuous color (`scatter`/`line` with a numeric
color column), a single figure-level colorbar is drawn with the global data
range, so panel colors are directly comparable. When `.legend()` is called on
a faceted chart, a single figure-level legend is drawn (deduped by label)
instead of one legend per panel.

### Pair plot

```python
# All numeric columns — scatter matrix with histograms on diagonal
gufo.pairplot(df).show()

# Color by a categorical column
gufo.pairplot(df, color="species").show()

# Subset of columns
gufo.pairplot(df, columns=["col_a", "col_b", "col_c"]).show()

# Returns a Grid — all grid methods work
gufo.pairplot(df, color="species").title("Iris").save("pairs.png")
```

### Joint plot

```python
# Scatter with marginal histograms
gufo.jointplot(df, "x", "y").show()

# Color by a categorical column
gufo.jointplot(df, "x", "y", color="species").show()

# KDE marginals instead of histograms
gufo.jointplot(df, "x", "y", marginal="kde").show()

# Returns a Grid — all grid methods work
gufo.jointplot(df, "x", "y").title("Joint").save("joint.png")
```

### Two-variable faceting

```python
# Row by income group, column by continent
gufo.chart(df).scatter("gdp", "life_exp").facet("continent", row="income_group").show()

# Row only — one panel per category, stacked vertically
gufo.chart(df).scatter("gdp", "life_exp").facet(row="income_group").show()
```

---

## Saving

```python
gufo.chart(df).scatter("x", "y").save("chart.png")
gufo.chart(df).scatter("x", "y").save("chart.svg")
gufo.chart(df).scatter("x", "y").save("chart.pdf")
gufo.chart(df).scatter("x", "y").save("chart.png", dpi=300)
```

---

## Figure size

```python
gufo.chart(df).scatter("x", "y").size(12, 6).show()
```

---

## Matplotlib escape hatch

When you need something gufo does not support natively, `.apply()` gives you direct access to the underlying matplotlib figure and axes. It stays in the chain and returns the chart for further method calls.

```python
(
    gufo.chart(df)
    .scatter("x", "y")
    .apply(lambda figure, axes: axes.axhline(y=0, color="gray", linewidth=0.5))
    .show()
)
```

For more complex operations, use a named function:

```python
def add_custom_annotations(figure, axes):
    for x_val in [2001, 2008, 2020]:
        axes.axvline(x_val, color="red", alpha=0.3, linewidth=0.8)

gufo.chart(df).line("year", "gdp").apply(add_custom_annotations).show()
```

`.apply()` is the escape hatch for anything gufo does not yet cover natively. If you find yourself using it for the same thing repeatedly, it is a good candidate for a native gufo feature — open an issue.

---

## Jupyter Notebooks

Gufo charts render inline automatically. Calling `.show()` displays the chart in the current cell output. No additional configuration needed.

---

## Installation

```bash
pip install gufo              # core only (matplotlib + numpy)
pip install gufo[pandas]      # + pandas support
pip install gufo[polars]      # + polars support
pip install gufo[scipy]       # + KDE, swarm
pip install gufo[stats]       # + LOWESS smoothing
pip install gufo[all]         # everything
```

Without pandas or polars, gufo works with dicts, numpy arrays, and raw lists. KDE and swarm plots require scipy. LOWESS smoothing requires statsmodels.

## PyData stack compatibility

| Library | Install extra | Status |
|---------|--------------|--------|
| pandas  | `gufo[pandas]` | Full support |
| numpy   | (included) | Full support |
| polars  | `gufo[polars]` | Full support |
| scipy   | `gufo[scipy]` | KDE, swarm |
| statsmodels | `gufo[stats]` | LOWESS smoothing |

---

## Development

```bash
# Install in editable mode with all dependencies (requires uv)
uv sync --group dev

# Run the test suite
pytest tests/ -v
```

---

## Roadmap

**v0.0.1** — scatter, line, bar, histogram, theming, wide-form data, grid layout, faceting, input validation

**v0.0.2** — box plot, heatmap, area chart, violin plot, polars support

**v0.0.3** — pair plot

**v0.0.4** — regression overlay, KDE/density plot, strip/swarm plots (scipy optional dependency) ✓

**v0.0.5** — categorical color on box/violin, countplot, error bars, rugplot, ECDF, color palette API, reference lines/bands ✓

**v0.0.6** — stacked/dodged bar grouping, continuous color scales on scatter, jointplot, Grid width/height ratios, horizontal histogram, complete docstrings, visual gallery, tutorial ✓

**v0.0.7** — data labels, pointplot, LOWESS smoothing, facet sharex/sharey, legend outside positioning ✓

**v0.0.8** — shared colorbar/legend on faceted charts, continuous color on line, `.label()` on line and pointplot, error bands on area ✓

**v0.0.9** — release-hygiene pass ahead of PyPI (changelog cleanup, README polish, TestPyPI dry run)

**v0.1.0** — first tagged release on PyPI ✓

**v0.1.1** — bug fixes: layer mutation during render, facet NaN handling, kdeplot kwargs passthrough, improved error messages for array input

**v0.1.2** — docstring fix for Sphinx, updated project logo

**v0.2.0** — category ordering (`order=`, `color_order=`), histogram grouping modes (`multiple=`), step histogram (`fill=False`), dev dependency groups
