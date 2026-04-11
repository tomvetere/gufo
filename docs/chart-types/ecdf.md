# ECDF

An empirical cumulative distribution function (ECDF) shows the proportion
of observations at or below each value.

```python
cerno.chart(df).ecdf("score").show()
```

## Color

Split by a categorical column to compare distributions.

```python
cerno.chart(df).ecdf("score", color="group").legend().show()
```

## API reference

See {py:meth}`cerno.core.chart.Chart.ecdf`.
