# Regression overlay

A regression overlay adds a fit line to a scatter plot. Pass a
`cerno.regression()` config to the `fit` parameter of `.scatter()`.

```python
cerno.chart(df).scatter("x", "y", fit=cerno.regression()).show()
```

## Polynomial fit

```python
cerno.chart(df).scatter("x", "y", fit=cerno.regression(degree=2)).show()
```

## Styling the fit line

```python
cerno.chart(df).scatter(
    "x", "y",
    fit=cerno.regression(color="red", linestyle="--", linewidth=3),
).show()
```

## With grouped scatter

When using categorical color encoding, the regression fits across all groups
(one line for the full dataset).

```python
cerno.chart(df).scatter(
    "x", "y", color="category", fit=cerno.regression()
).show()
```

## Custom label

```python
cerno.chart(df).scatter(
    "x", "y", fit=cerno.regression(label="Trend")
).legend().show()
```

By default, the label is "Linear fit" (degree 1) or "Poly(N) fit" (degree N).

## API reference

See {py:func}`cerno.regression` and {py:class}`cerno.stats.regression.Regression`.
