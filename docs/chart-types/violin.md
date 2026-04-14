# Violin plot

A violin plot shows the distribution shape of a numeric variable grouped by
categories.

```python
gufo.chart(df).violin("department", "salary").show()
```

## Horizontal

```python
gufo.chart(df).violin("department", "salary", horizontal=True).show()
```

## Color

```python
# Single color for all violins
gufo.chart(df).violin("department", "salary", color="steelblue").show()
```

## Wide-form

Pass a list of column names to show one violin per column — no reshaping needed.

```python
gufo.chart(df).violin("x", ["q1_scores", "q2_scores", "q3_scores"]).show()
```

## API reference

See {py:meth}`gufo.core.chart.Chart.violin`.
