# Area

An area chart shows a filled region between a line and the x-axis.

```python
cerno.chart(df).area("x", "y").show()
```

## Stacked area (wide-form)

Pass a list of column names for a stacked area chart — no reshaping needed.

```python
cerno.chart(df).area("x", ["series_a", "series_b"]).show()
```

## Color and transparency

```python
# Literal color with custom alpha
cerno.chart(df).area("x", "y", color="steelblue", alpha=0.3).show()

# Grouped by category
cerno.chart(df).area("x", "y", color="category").show()
```

## Error band

Pass `y_error` to draw a lighter fill band around the top edge of the area.

```python
cerno.chart(df).area("x", "y", y_error="y_std").show()
```

## API reference

See {py:meth}`cerno.core.chart.Chart.area`.
