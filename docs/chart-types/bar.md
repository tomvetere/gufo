# Bar

A bar chart compares values across discrete categories.

```python
cerno.chart(df).bar("region", "sales").show()
```

## Horizontal bars

```python
cerno.chart(df).bar("region", "sales", horizontal=True).show()
```

## Color

```python
# Color each bar by its category
cerno.chart(df).bar("region", "sales", color="region").show()

# Single color for all bars
cerno.chart(df).bar("region", "sales", color="#4C72B0").show()
```

## API reference

See {py:meth}`cerno.core.chart.Chart.bar`.
