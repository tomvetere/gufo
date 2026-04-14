# Box plot

A box plot shows the distribution of a numeric variable grouped by categories.

```python
gufo.chart(df).boxplot("department", "salary").show()
```

## Horizontal

```python
gufo.chart(df).boxplot("department", "salary", horizontal=True).show()
```

## Color

```python
# Single color for all boxes
gufo.chart(df).boxplot("department", "salary", color="steelblue").show()
```

## Wide-form

Pass a list of column names to show one box per column — no reshaping needed.

```python
gufo.chart(df).boxplot("x", ["q1_scores", "q2_scores", "q3_scores"]).show()
```

## API reference

See {py:meth}`gufo.core.chart.Chart.boxplot`.
