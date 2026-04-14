# Bar

A bar chart compares values across discrete categories.

```python
gufo.chart(df).bar("region", "sales").show()
```

## Horizontal bars

```python
gufo.chart(df).bar("region", "sales", horizontal=True).show()
```

## Color

```python
# Single color for all bars
gufo.chart(df).bar("region", "sales", color="#4C72B0").show()
```

## Grouped (dodged) bars

When `color` is a categorical column, bars are grouped side-by-side within
each x category.

```python
gufo.chart(df).bar("quarter", "revenue", color="region").legend().show()

# Horizontal grouped bars
gufo.chart(df).bar("quarter", "revenue", color="region", horizontal=True).legend().show()
```

## Stacked bars

Set `stacked=True` to stack bars instead of dodging them.

```python
gufo.chart(df).bar("quarter", "revenue", color="region", stacked=True).legend().show()
```

## Wide-form grouped bars

Pass a list of column names to `y` for grouped bars from wide-form data.

```python
gufo.chart(df).bar("quarter", ["product_a", "product_b"]).show()
```

## Data labels

Add value labels to bars with `.label()`.

```python
gufo.chart(df).bar("region", "sales").label().show()

# Custom formatting
gufo.chart(df).bar("region", "sales").label(fmt=".1f").show()
```

## API reference

See {py:meth}`gufo.core.chart.Chart.bar`.
