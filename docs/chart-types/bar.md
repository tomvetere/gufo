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
# Single color for all bars
cerno.chart(df).bar("region", "sales", color="#4C72B0").show()
```

## Grouped (dodged) bars

When `color` is a categorical column, bars are grouped side-by-side within
each x category.

```python
cerno.chart(df).bar("quarter", "revenue", color="region").legend().show()

# Horizontal grouped bars
cerno.chart(df).bar("quarter", "revenue", color="region", horizontal=True).legend().show()
```

## Stacked bars

Set `stacked=True` to stack bars instead of dodging them.

```python
cerno.chart(df).bar("quarter", "revenue", color="region", stacked=True).legend().show()
```

## Wide-form grouped bars

Pass a list of column names to `y` for grouped bars from wide-form data.

```python
cerno.chart(df).bar("quarter", ["product_a", "product_b"]).show()
```

## API reference

See {py:meth}`cerno.core.chart.Chart.bar`.
