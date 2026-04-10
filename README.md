<p align="center">
  <img src="docs/_static/cerno_logo.png" alt="Cerno logo" width="200">
</p>

# Cerno

**Data visualization for humans.**

Cerno is a Python data visualization library built on matplotlib. It is designed for researchers, data explorers, and anyone making charts for reports or presentations who wants results fast without fighting their tools.

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
```

### Bar

```python
cerno.chart(df).bar("region", "sales").show()

# Horizontal
cerno.chart(df).bar("region", "sales", horizontal=True).show()

# Colored by category
cerno.chart(df).bar("region", "sales", color="region").show()

# Grouped bars from wide-form data
cerno.chart(df).bar("quarter", ["product_a", "product_b"]).show()

# Grouped bars, horizontal
cerno.chart(df).bar("quarter", ["product_a", "product_b"], horizontal=True).show()
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
```

### Box plot

```python
cerno.chart(df).boxplot("department", "salary").show()

# Horizontal
cerno.chart(df).boxplot("department", "salary", horizontal=True).show()

# Colored boxes
cerno.chart(df).boxplot("department", "salary", color="steelblue").show()

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
    .line("year", "gdp")
    .apply(lambda figure, axes: axes.axvspan(2008, 2009, alpha=0.15, color="gray"))
    .title("GDP with Recession Band")
    .show()
)
```

For more complex operations, use a named function:

```python
def add_recession_bands(figure, axes):
    for start, end in [(2001, 2001), (2008, 2009), (2020, 2020)]:
        axes.axvspan(start, end, alpha=0.15, color="gray")

cerno.chart(df).line("year", "gdp").apply(add_recession_bands).show()
```

`.apply()` is intentionally the only escape hatch in v0.1. If you find yourself using it for the same thing repeatedly, it is a good candidate for a native cerno feature — open an issue.

---

## Jupyter Notebooks

Cerno charts render inline automatically. Calling `.show()` displays the chart in the current cell output. No additional configuration needed.

---

## Installation

```bash
pip install cerno              # core only (matplotlib + numpy)
pip install cerno[pandas]      # + pandas support
pip install cerno[polars]      # + polars support
pip install cerno[all]         # everything
```

Without pandas or polars, cerno works with dicts, numpy arrays, and raw lists.

## PyData stack compatibility

| Library | Install extra | Status |
|---------|--------------|--------|
| pandas  | `cerno[pandas]` | Full support |
| numpy   | (included) | Full support |
| polars  | `cerno[polars]` | Full support |

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

**v0.4** — regression overlay, KDE/density plot, strip/swarm plots (scipy optional dependency)
