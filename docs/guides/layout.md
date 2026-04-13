# Layout

## Multi-panel grid

Use `cerno.grid()` to build a fixed rows x cols layout. It returns a `Grid` — a dedicated layout container for multiple charts.

```python
import cerno

g = cerno.grid(rows=2, cols=2, figsize=(14, 10))

g[0, 0] = cerno.chart(df).scatter("x", "y").title("Panel A")
g[0, 1] = cerno.chart(df).line("year", "revenue").title("Panel B")
g[1, 0] = cerno.chart(df).histogram("income").title("Panel C")
g[1, 1] = cerno.chart(df2).bar("region", "sales").title("Panel D")

g.show()
```

Each panel is a normal `Chart` built the usual way with `cerno.chart(data)`.
Assign it to a grid cell with `g[row, col] = ...`. All `Chart` methods
(marks, labels, themes, axis control) work on panels exactly as they do on
standalone charts.

### Grid-level options

```python
# Add a super-title above all panels
g = cerno.grid(2, 2).title("Dashboard")

# Different data per panel
g[0, 0] = cerno.chart(sales_df).scatter("x", "y")
g[0, 1] = cerno.chart(weather_df).line("date", "temp")
```

### Saving a grid

```python
g.save("dashboard.png", dpi=300)
g.save("report.pdf")
```

### Empty cells

Any cell you don't assign is automatically hidden. You don't need to fill every cell.

```python
g = cerno.grid(2, 2)
g[0, 0] = cerno.chart(df).scatter("x", "y")
# Other 3 cells stay blank
g.save("sparse.png")
```

## Faceting

Faceting creates one panel per value of a categorical column automatically.

```python
# Split into one subplot per continent
cerno.chart(df).scatter("gdp", "life_exp").facet("continent").show()

# Control the number of columns before wrapping
cerno.chart(df).scatter("gdp", "life_exp").facet("continent", cols=4).show()
```

### Two-variable faceting

Use `row` to add a second dimension. Row categories go down, column categories go across.

```python
# Row by income group, column by continent
cerno.chart(df).scatter("gdp", "life_exp").facet("continent", row="income_group").show()

# Row only — one panel per category, stacked vertically
cerno.chart(df).scatter("gdp", "life_exp").facet(row="income_group").show()
```

Chart-level `.title()` becomes a super-title above all panels. Empty cells are hidden automatically.

### Shared / independent axes

By default, facet panels share axis ranges. Set `sharex=False` or `sharey=False`
to let each panel scale independently — useful when groups have very different ranges.

```python
cerno.chart(df).scatter("x", "y").facet("group", sharey=False).show()
```

### Shared colorbar and legend

When a faceted chart uses continuous color (a numeric column as `color=` on
`scatter` or `line`), a single figure-level colorbar is drawn using the
global data range across all panels, so colors are directly comparable. When
`.legend()` is called on a faceted chart, a single figure-level legend is
drawn (deduped by label) instead of one per panel.

## Joint plot

`cerno.jointplot()` creates a scatter plot with marginal distributions
(histograms or KDE) on the top and right edges. It returns a `Grid`.

```python
cerno.jointplot(df, "x", "y").show()

# KDE marginals
cerno.jointplot(df, "x", "y", marginal="kde").show()

# Color by category
cerno.jointplot(df, "x", "y", color="species").show()
```

## Pair plot

`cerno.pairplot()` generates an N×N grid of scatter plots and histograms for all numeric columns. It returns a `Grid`, so all grid methods work.

```python
cerno.pairplot(df).show()
cerno.pairplot(df, color="species").title("Iris Dataset").save("pairs.png")
```

See {doc}`pairplot` for full details.

## API reference

See {py:class}`cerno.layout.grid.Grid` — specifically `.__setitem__`, `.title()`, `.theme()`, `.apply()`, `.show()`, `.save()`.
