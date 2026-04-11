<p align="center">
  <img src="docs/_static/cerno_logo.png" alt="Cerno logo" width="200">
</p>

# Cerno

**Data visualization for humans.**

*Cerno* (Classical Latin: /ˈker.noː/, **KEHR-noh**) — "I discern, I perceive, I distinguish."

A Python data visualization library built on matplotlib. Designed for researchers, data explorers, and anyone making charts for reports or presentations who wants results fast without fighting their tools.

```python
import cerno

(
    cerno.chart(df)
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
pip install cerno
```

---

## Core principles

- **One API, one pattern.** Everything goes through `cerno.chart(data)`. No switching between function styles depending on what you want to do.
- **Works with your data as-is.** Pass a pandas DataFrame, Polars DataFrame, a numpy array, a dict, or raw lists — cerno handles the shape without requiring you to reshape first.
- **Matplotlib when you need it.** Cerno covers the common cases cleanly. When you need something custom, `.apply()` drops you into matplotlib without starting over.
- **Modern defaults.** Charts look good without any configuration.

---

## Quick Start

```python
import cerno
import pandas as pd

df = pd.read_csv("gapminder.csv")

cerno.chart(df).scatter("gdp_per_capita", "life_expectancy").show()
```

Polars works the same way:

```python
import polars as pl

df = pl.read_csv("gapminder.csv")
cerno.chart(df).scatter("gdp_per_capita", "life_expectancy").show()
```

---

## Chart types

### Scatter

```python
cerno.chart(df).scatter("x", "y").show()

# Encode a third variable as color or size
cerno.chart(df).scatter("x", "y", color="category", size="population").show()

# Transparency for dense data
cerno.chart(df).scatter("x", "y", alpha=0.4).show()

# Multiple series from wide-form data — no pd.melt() needed
cerno.chart(df).scatter("x", ["series_a", "series_b"]).show()

# Error bars
cerno.chart(df).scatter("x", "y", y_error="y_std").show()
cerno.chart(df).scatter("x", "y", y_error="y_std", x_error="x_std").show()
```

### Line

```python
cerno.chart(df).line("year", "revenue").show()

# Multiple series from wide-form data — no pd.melt() needed
wide_df = pd.DataFrame({
    "year":      [2020, 2021, 2022, 2023],
    "product_a": [100,  130,  160,  210],
    "product_b": [80,   95,   115,  140],
    "product_c": [60,   70,   90,   125],
})
cerno.chart(wide_df).line("year", ["product_a", "product_b", "product_c"]).show()

# Multiple series from long-form data
cerno.chart(long_df).line("year", "revenue", color="product").show()

# Dashed line style
cerno.chart(df).line("year", "forecast", stroke_dash="dashed").show()

# Error bars / confidence band
cerno.chart(df).line("year", "revenue", y_error="revenue_std").show()
```

### Bar

```python
cerno.chart(df).bar("region", "sales").show()

# Horizontal
cerno.chart(df).bar("region", "sales", horizontal=True).show()

# Colored by category
cerno.chart(df).bar("region", "sales", color="region").show()

# Grouped (dodged) bars by category
cerno.chart(df).bar("quarter", "revenue", color="region").legend().show()

# Stacked bars
cerno.chart(df).bar("quarter", "revenue", color="region", stacked=True).legend().show()

# Grouped bars from wide-form data
cerno.chart(df).bar("quarter", ["product_a", "product_b"]).show()

# Grouped bars, horizontal
cerno.chart(df).bar("quarter", ["product_a", "product_b"], horizontal=True).show()

# Error bars
cerno.chart(df).bar("region", "sales", y_error="sales_std").show()
```

### Histogram

```python
cerno.chart(df).histogram("income").show()

# Custom bin count
cerno.chart(df).histogram("income", bins=40).show()

# From a raw array
import numpy as np
data = np.random.normal(0, 1, 1000)
cerno.chart().histogram(data).show()

# With a KDE overlay (requires scipy)
cerno.chart(df).histogram("income", kde=cerno.kde()).show()

# Filled KDE overlay
cerno.chart(df).histogram("income", kde=cerno.kde(fill=True, alpha=0.3)).show()
```

### Box plot

```python
cerno.chart(df).boxplot("department", "salary").show()

# Horizontal
cerno.chart(df).boxplot("department", "salary", horizontal=True).show()

# Colored boxes
cerno.chart(df).boxplot("department", "salary", color="steelblue").show()

# Grouped by a categorical variable — side-by-side boxes
cerno.chart(df).boxplot("department", "salary", color="gender").legend().show()

# Multiple columns from wide-form data — each column becomes a box
cerno.chart(df).boxplot("x", ["q1_scores", "q2_scores", "q3_scores"]).show()
```

### Violin plot

```python
cerno.chart(df).violin("department", "salary").show()

# Horizontal
cerno.chart(df).violin("department", "salary", horizontal=True).show()

# Colored violins
cerno.chart(df).violin("department", "salary", color="steelblue").show()

# Grouped by a categorical variable — side-by-side violins
cerno.chart(df).violin("department", "salary", color="gender").legend().show()

# Multiple columns from wide-form data — each column becomes a violin
cerno.chart(df).violin("x", ["q1_scores", "q2_scores", "q3_scores"]).show()
```

### Heatmap

```python
# Matrix form — DataFrame is the heatmap
cerno.chart(pivot_df).heatmap().show()

# Long-form — pivoted internally
cerno.chart(df).heatmap("x_col", "y_col", color="value").show()

# Custom colormap and cell annotations
cerno.chart(pivot_df).heatmap(cmap="coolwarm", annotate=True).show()
```

### Area

```python
cerno.chart(df).area("x", "y").show()

# Stacked area from wide-form data
cerno.chart(df).area("x", ["series_a", "series_b"]).show()

# Colored area with transparency
cerno.chart(df).area("x", "y", color="steelblue", alpha=0.3).show()

# Grouped by category
cerno.chart(df).area("x", "y", color="category").show()
```

### Regression overlay

```python
# Linear fit on a scatter plot
cerno.chart(df).scatter("x", "y", fit=cerno.regression()).show()

# Polynomial fit
cerno.chart(df).scatter("x", "y", fit=cerno.regression(degree=2)).show()

# Styled fit line
cerno.chart(df).scatter("x", "y", fit=cerno.regression(color="red", linestyle="--")).show()

# Regression with grouped scatter — one line fits all groups
cerno.chart(df).scatter("x", "y", color="category", fit=cerno.regression()).show()
```

### LOWESS smoothing

```python
# Non-parametric smooth on a scatter plot (requires statsmodels)
cerno.chart(df).scatter("x", "y", fit=cerno.lowess()).show()

# Custom smoothing fraction
cerno.chart(df).scatter("x", "y", fit=cerno.lowess(frac=0.3)).show()
```

### KDE (kernel density estimation)

```python
# Standalone density plot (requires scipy)
cerno.chart(df).kde("x").show()

# Filled density
cerno.chart(df).kde("x", fill=True).show()

# Grouped by category
cerno.chart(df).kde("x", color="category").show()
```

### Strip plot

```python
# Jittered points along a categorical axis
cerno.chart(df).strip("department", "salary").show()

# Horizontal
cerno.chart(df).strip("department", "salary", horizontal=True).show()

# Custom jitter width and color
cerno.chart(df).strip("department", "salary", jitter=0.3, color="steelblue").show()

# Wide-form data
cerno.chart(df).strip(None, ["q1_scores", "q2_scores"]).show()
```

### Swarm plot

```python
# Non-overlapping points along a categorical axis (requires scipy)
cerno.chart(df).swarm("department", "salary").show()

# Horizontal
cerno.chart(df).swarm("department", "salary", horizontal=True).show()

# Colored
cerno.chart(df).swarm("department", "salary", color="coral").show()

# Wide-form data
cerno.chart(df).swarm(None, ["q1_scores", "q2_scores"]).show()
```

### Countplot

```python
# Bar chart of value counts
cerno.chart(df).countplot("department").show()

# Horizontal
cerno.chart(df).countplot("department", horizontal=True).show()

# Grouped by a second categorical variable
cerno.chart(df).countplot("department", color="gender").legend().show()
```

### ECDF

```python
# Empirical cumulative distribution function
cerno.chart(df).ecdf("income").show()

# Grouped by category
cerno.chart(df).ecdf("income", color="region").legend().show()
```

### Rugplot

```python
# Tick marks showing individual data points along the x axis
cerno.chart(df).rug("income").show()

# Commonly layered with a histogram or KDE
cerno.chart(df).histogram("income").rug("income").show()

# Custom height and transparency
cerno.chart(df).rug("income", height=0.1, alpha=0.8).show()

# Colored by category
cerno.chart(df).rug("income", color="region").legend().show()
```

### Point plot

```python
# Mean + 95% CI per category
cerno.chart(df).pointplot("day", "total_bill").show()

# Grouped by a second variable
cerno.chart(df).pointplot("day", "total_bill", color="sex").legend().show()
```

---

## Data labels

```python
# Label bars with their values
cerno.chart(df).bar("region", "sales").label().show()

# Custom formatting
cerno.chart(df).bar("region", "sales").label(fmt=".1f").show()

# Label scatter points with a column
cerno.chart(df).scatter("x", "y").label("name").show()
```

---

## Layering

Multiple marks can be added to the same chart. Each call registers a new layer rendered in order.

```python
(
    cerno.chart(df)
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
cerno.chart(df).scatter("x", "y").hline(50, label="Target").legend().show()

# Vertical reference line
cerno.chart(df).line("year", "revenue").vline(2020, color="red", label="Launch").legend().show()

# Horizontal band (shaded region)
cerno.chart(df).scatter("x", "y").hband(40, 60, color="green", alpha=0.1).show()

# Vertical band
cerno.chart(df).line("year", "gdp").vband(2008, 2009, label="Recession").show()

# Combine multiple references
(
    cerno.chart(df)
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
cerno.chart(df).scatter("x", "y", color="category").palette("colorblind").show()

# Available named palettes: 'cerno' (default), 'pastel', 'bold', 'colorblind'

# Custom palette — pass a list of color strings
cerno.chart(df).bar("quarter", ["q1", "q2", "q3"]).palette(["#e63946", "#457b9d", "#2a9d8f"]).show()
```

---

## Labels and annotations

```python
(
    cerno.chart(df)
    .scatter("x", "y")
    .title("Chart Title")
    .subtitle("A clarifying subtitle shown below the title")
    .xlabel("Horizontal axis label")
    .ylabel("Vertical axis label")
    .caption("Source: World Bank, 2024")   # small text below the chart
    .show()
)

# Arrow annotation pointing to a specific data point
cerno.chart(df).scatter("x", "y").annotate("Outlier", xy=(42, 180)).show()
```

---

## Axis control

```python
(
    cerno.chart(df)
    .scatter("x", "y")
    .xlim(0, 100)
    .ylim(0, 500)
    .xscale("log")
    .xticks(rotation=45)
    .show()
)
```

---

## Legend

```python
# Basic legend
cerno.chart(df).scatter("x", "y", color="cat").legend().show()

# With title
cerno.chart(df).scatter("x", "y", color="cat").legend(title="Category").show()

# Positioned outside the axes
cerno.chart(df).scatter("x", "y", color="cat").legend(position="outside right").show()
cerno.chart(df).scatter("x", "y", color="cat").legend(position="outside bottom").show()

# Hidden
cerno.chart(df).scatter("x", "y", color="cat").legend(hide=True).show()
```

---

## Data input formats

Cerno accepts any of these without conversion:

```python
# Pandas DataFrame (long-form or wide-form)
cerno.chart(df).scatter("x", "y").show()

# Dict
cerno.chart({"x": [1, 2, 3], "y": [4, 5, 6]}).scatter("x", "y").show()

# Raw arrays or lists (no data argument needed)
cerno.chart().scatter([1, 2, 3], [4, 5, 6]).show()

import numpy as np
cerno.chart().line(np.arange(100), np.random.cumsum(np.random.randn(100))).show()
```

---

## Theming

```python
# Apply a theme globally (affects all subsequent charts)
cerno.set_theme("cerno_modern")   # default
cerno.set_theme("cerno_dark")
cerno.set_theme("cerno_print")    # black and white, print-safe

# Apply a theme to one chart only
cerno.chart(df).theme("cerno_dark").scatter("x", "y").show()

# Apply a theme temporarily with a context manager
with cerno.theme_context("cerno_print"):
    cerno.chart(df).scatter("x", "y").save("print_ready.pdf")

# Create and register a custom theme
my_theme = cerno.get_theme("cerno_modern").merge({
    "axes.facecolor": "#1a1a2e",
    "figure.facecolor": "#16213e",
}).rename("brand_dark")

cerno.register_theme(my_theme)
cerno.set_theme("brand_dark")
```

---

## Layout

### Multi-panel grid

```python
g = cerno.grid(rows=2, cols=2, figsize=(14, 10))

g[0, 0] = cerno.chart(df).scatter("x", "y").title("Panel A")
g[0, 1] = cerno.chart(df).line("year", "revenue").title("Panel B")
g[1, 0] = cerno.chart(df).histogram("income").title("Panel C")
g[1, 1] = cerno.chart(df2).bar("region", "sales").title("Panel D")

g.show()
```

`cerno.grid()` returns a `Grid`, a layout container for multiple charts. Assign
panels with `g[row, col] = cerno.chart(data).mark(...)`. Each panel is a normal
`Chart`, so all methods work as usual. Grid-level `.title()` becomes a super-title.

### Faceting by a data column

```python
# Split into one subplot per continent
cerno.chart(df).scatter("gdp", "life_exp").facet("continent").show()

# Control the number of columns before wrapping
cerno.chart(df).scatter("gdp", "life_exp").facet("continent", cols=4).show()
```

`facet()` takes a categorical column name and creates one panel per unique value,
each showing the same layers with only that subset of data. Chart-level `.title()`
becomes a super-title above all panels. Empty cells are hidden automatically.

### Pair plot

```python
# All numeric columns — scatter matrix with histograms on diagonal
cerno.pairplot(df).show()

# Color by a categorical column
cerno.pairplot(df, color="species").show()

# Subset of columns
cerno.pairplot(df, columns=["col_a", "col_b", "col_c"]).show()

# Returns a Grid — all grid methods work
cerno.pairplot(df, color="species").title("Iris").save("pairs.png")
```

### Joint plot

```python
# Scatter with marginal histograms
cerno.jointplot(df, "x", "y").show()

# Color by a categorical column
cerno.jointplot(df, "x", "y", color="species").show()

# KDE marginals instead of histograms
cerno.jointplot(df, "x", "y", marginal="kde").show()

# Returns a Grid — all grid methods work
cerno.jointplot(df, "x", "y").title("Joint").save("joint.png")
```

### Two-variable faceting

```python
# Row by income group, column by continent
cerno.chart(df).scatter("gdp", "life_exp").facet("continent", row="income_group").show()

# Row only — one panel per category, stacked vertically
cerno.chart(df).scatter("gdp", "life_exp").facet(row="income_group").show()
```

---

## Saving

```python
cerno.chart(df).scatter("x", "y").save("chart.png")
cerno.chart(df).scatter("x", "y").save("chart.svg")
cerno.chart(df).scatter("x", "y").save("chart.pdf")
cerno.chart(df).scatter("x", "y").save("chart.png", dpi=300)
```

---

## Figure size

```python
cerno.chart(df).scatter("x", "y").size(12, 6).show()
```

---

## Matplotlib escape hatch

When you need something cerno does not support natively, `.apply()` gives you direct access to the underlying matplotlib figure and axes. It stays in the chain and returns the chart for further method calls.

```python
(
    cerno.chart(df)
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

cerno.chart(df).line("year", "gdp").apply(add_custom_annotations).show()
```

`.apply()` is the escape hatch for anything cerno does not yet cover natively. If you find yourself using it for the same thing repeatedly, it is a good candidate for a native cerno feature — open an issue.

---

## Jupyter Notebooks

Cerno charts render inline automatically. Calling `.show()` displays the chart in the current cell output. No additional configuration needed.

---

## Installation

```bash
pip install cerno              # core only (matplotlib + numpy)
pip install cerno[pandas]      # + pandas support
pip install cerno[polars]      # + polars support
pip install cerno[scipy]       # + KDE, swarm
pip install cerno[stats]       # + LOWESS smoothing
pip install cerno[all]         # everything
```

Without pandas or polars, cerno works with dicts, numpy arrays, and raw lists. KDE and swarm plots require scipy. LOWESS smoothing requires statsmodels.

## PyData stack compatibility

| Library | Install extra | Status |
|---------|--------------|--------|
| pandas  | `cerno[pandas]` | Full support |
| numpy   | (included) | Full support |
| polars  | `cerno[polars]` | Full support |
| scipy   | `cerno[scipy]` | KDE, swarm |
| statsmodels | `cerno[stats]` | LOWESS smoothing |

---

## Development

```bash
# Install in editable mode with all dependencies
pip install -e ".[all,docs]"
pip install pytest

# Run the test suite
pytest tests/ -v
```

---

## Roadmap

**v0.1** — scatter, line, bar, histogram, theming, wide-form data, grid layout, faceting, input validation

**v0.2** — box plot, heatmap, area chart, violin plot, polars support

**v0.3** — pair plot

**v0.4** — regression overlay, KDE/density plot, strip/swarm plots (scipy optional dependency) ✓

**v0.5** — categorical color on box/violin, countplot, error bars, rugplot, ECDF, color palette API, reference lines/bands ✓

**v0.6** — stacked/dodged bar grouping, continuous color scales on scatter, jointplot, Grid width/height ratios, horizontal histogram, complete docstrings, visual gallery, tutorial ✓

**v0.7** — data labels, pointplot, LOWESS smoothing, facet sharex/sharey, legend outside positioning
