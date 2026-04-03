# Layout

## Multi-panel grid

Use `cerno.grid()` (or `cerno.chart().grid()`) to build a fixed rows x cols layout. It returns a `Chart` — the same type you use for single charts.

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
Planned for v0.2.

```python
# Planned API (v0.2)
cerno.chart(df).scatter("gdp", "life_exp").facet("continent").show()

# With row and column variables
cerno.chart(df).scatter("x", "y").facet(row="region", col="decade").show()
```

## API reference

See {py:class}`cerno.core.chart.Chart` — specifically `.grid()`, `.__setitem__`.
