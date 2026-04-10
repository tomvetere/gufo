# Strip plot

A strip plot shows individual data points along a categorical axis, with
random jitter to reduce overplotting.

```python
cerno.chart(df).strip("department", "salary").show()
```

## Horizontal

```python
cerno.chart(df).strip("department", "salary", horizontal=True).show()
```

## Jitter width

Control the amount of random spread. Default is `0.2`.

```python
cerno.chart(df).strip("department", "salary", jitter=0.4).show()
```

## Color

```python
cerno.chart(df).strip("department", "salary", color="steelblue").show()
```

## Wide-form data

Pass a list of column names as `y` to create one strip per column.

```python
cerno.chart(df).strip(None, ["q1_scores", "q2_scores", "q3_scores"]).show()
```

## API reference

See {py:meth}`cerno.core.chart.Chart.strip`.
