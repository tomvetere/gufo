# Getting started

## Installation

```bash
pip install cerno              # core only (matplotlib + numpy)
pip install cerno[pandas]      # + pandas support
pip install cerno[polars]      # + polars support
pip install cerno[scipy]       # + KDE and swarm plots
pip install cerno[all]         # everything
```

For the latest development version:

```bash
pip install git+https://github.com/thomas/cerno.git
```

## Your first chart

```python
import cerno
import pandas as pd

df = pd.read_csv("gapminder.csv")

cerno.chart(df).scatter("gdp_per_capita", "life_expectancy").show()
```

## The pattern

Every cerno chart follows the same structure:

1. **Create a chart** with `cerno.chart(data)` — pass your data once here.
2. **Add marks** — `.scatter()`, `.line()`, `.bar()`, `.histogram()`, `.boxplot()`, `.violin()`, `.heatmap()`, `.area()`, `.kde()`, `.strip()`, `.swarm()`.
3. **Describe the chart** — `.title()`, `.xlabel()`, `.ylabel()`, `.legend()`.
4. **Output** — `.show()` to display, `.save("file.png")` to write to disk.

```python
(
    cerno.chart(df)
    .scatter("x", "y", color="category")   # mark
    .title("My Chart")                      # description
    .xlabel("X axis")
    .ylabel("Y axis")
    .legend()
    .show()                                 # output
)
```

Methods can be called in any order. `.show()` and `.save()` trigger rendering —
everything before them just registers intent.

## What data cerno accepts

You do not need to reshape your data before passing it in:

- **pandas DataFrame** — long-form or wide-form, refer to columns by name
- **Polars DataFrame** — same as pandas, install with `cerno[polars]`
- **dict** — `{"x": [...], "y": [...]}`
- **numpy arrays or lists** — pass directly to mark methods, omit data from `cerno.chart()`

See [Data formats](guides/data-formats.md) for details and examples.

## Running the tests

If you are contributing or want to verify your installation:

```bash
pip install pytest
pytest tests/ -v
```

## Tutorial: exploring a dataset

This walkthrough uses a small inline dataset — no external files needed.

### Step 1 — create some data

```python
import cerno
import pandas as pd

sales = pd.DataFrame({
    "month":    ["Jan", "Feb", "Mar", "Apr", "May", "Jun"] * 2,
    "revenue":  [120, 150, 170, 160, 200, 220, 90, 110, 130, 125, 160, 180],
    "region":   ["East"] * 6 + ["West"] * 6,
    "headcount": [10, 12, 11, 13, 15, 14, 8, 9, 10, 10, 12, 11],
})
```

### Step 2 — a basic scatter plot

```python
cerno.chart(sales).scatter("headcount", "revenue").show()
```

One line, one chart. `cerno.chart(data)` binds the data, `.scatter()` says
what to draw, and `.show()` triggers rendering.

### Step 3 — add color, labels, and a title

```python
(
    cerno.chart(sales)
    .scatter("headcount", "revenue", color="region")
    .title("Revenue vs Headcount")
    .xlabel("Headcount")
    .ylabel("Revenue ($k)")
    .legend()
    .show()
)
```

Passing `color="region"` splits the points by category and adds a legend
entry for each group automatically.

### Step 4 — layer a regression fit

```python
(
    cerno.chart(sales)
    .scatter("headcount", "revenue", color="region",
             fit=cerno.regression())
    .title("Revenue vs Headcount — with fit")
    .xlabel("Headcount")
    .ylabel("Revenue ($k)")
    .legend()
    .show()
)
```

`cerno.regression()` creates a linear fit config. Pass `degree=2` for a
polynomial. The fit line is drawn per-group when `color` is set.

### Step 5 — facet by a column

```python
(
    cerno.chart(sales)
    .scatter("headcount", "revenue")
    .facet("region")
    .title("Revenue by Region")
    .show()
)
```

`.facet("region")` splits the data into one panel per unique value. Add
`row="another_col"` for a two-dimensional grid.

### Step 6 — save to a file

```python
(
    cerno.chart(sales)
    .scatter("headcount", "revenue", color="region")
    .title("Revenue vs Headcount")
    .save("revenue_scatter.png", dpi=300)
)
```

`.save()` writes the figure and closes it. Pass `dpi=` to control
resolution. Supported formats include PNG, PDF, SVG, and anything
matplotlib supports.

## Next steps

- [Gallery](gallery.md) — visual examples of every chart type
- [Chart types](chart-types/index.md) — detailed docs for every mark
- [Theming](guides/theming.md) — built-in themes and custom theme creation
- [Layout](guides/layout.md) — grids and faceting
- [API reference](api/index.md) — full method documentation
