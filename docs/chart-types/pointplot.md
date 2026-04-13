# Point plot

A point plot shows the mean of a numeric variable for each category,
connected by lines, with error bars representing the 95% confidence
interval (via standard error).

```python
cerno.chart(df).pointplot("day", "total_bill").show()
```

## Color grouping

Split by a second categorical column. Groups are dodged so they
don't overlap.

```python
cerno.chart(df).pointplot("day", "total_bill", color="sex").legend().show()
```

## Horizontal

```python
cerno.chart(df).pointplot("day", "total_bill", horizontal=True).show()
```

## Data labels

Use `.label()` to annotate each category mean with its value.

```python
cerno.chart(df).pointplot("day", "tip").label(fmt=".2f").show()
```

## API reference

See {py:meth}`cerno.core.chart.Chart.pointplot`.
