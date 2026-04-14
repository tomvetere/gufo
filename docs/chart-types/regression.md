# Regression overlay

A regression overlay adds a fit line to a scatter plot. Pass a
`gufo.regression()` config to the `fit` parameter of `.scatter()`.

```python
gufo.chart(df).scatter("x", "y", fit=gufo.regression()).show()
```

## Polynomial fit

```python
gufo.chart(df).scatter("x", "y", fit=gufo.regression(degree=2)).show()
```

## Styling the fit line

```python
gufo.chart(df).scatter(
    "x", "y",
    fit=gufo.regression(color="red", linestyle="--", linewidth=3),
).show()
```

## With grouped scatter

When using categorical color encoding, the regression fits across all groups
(one line for the full dataset).

```python
gufo.chart(df).scatter(
    "x", "y", color="category", fit=gufo.regression()
).show()
```

## Custom label

```python
gufo.chart(df).scatter(
    "x", "y", fit=gufo.regression(label="Trend")
).legend().show()
```

By default, the label is "Linear fit" (degree 1) or "Poly(N) fit" (degree N).

## API reference

See {py:func}`gufo.regression` and {py:class}`gufo.stats.regression.Regression`.
