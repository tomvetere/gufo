# Layout

## Multi-panel grid

Use `cerno.grid()` to build a fixed rows × cols layout with multiple panels.

```python
import cerno

grid = cerno.grid(rows=2, cols=2, figsize=(14, 10))

grid[0, 0].chart(df).scatter("x", "y").title("Panel A")
grid[0, 1].chart(df).line("year", "revenue").title("Panel B")
grid[1, 0].chart(df).histogram("income").title("Panel C")
grid[1, 1].chart(df2).bar("region", "sales").title("Panel D")

grid.show()
```

`grid[row, col]` returns a cell. Call `.chart(data)` on the cell to get a
standard `Chart` bound to that panel. All normal `Chart` methods work from there.

### Saving a grid

```python
grid.save("dashboard.png", dpi=300)
grid.save("report.pdf")
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

See {py:mod}`cerno.layout.grid`.
