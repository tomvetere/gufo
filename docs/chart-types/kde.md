# KDE (kernel density estimation)

A KDE plot shows the estimated probability density of a numeric variable.
Requires scipy (`pip install cerno[scipy]`).

## Standalone density plot

```python
cerno.chart(df).kde("x").show()
```

## Filled density

```python
cerno.chart(df).kde("x", fill=True).show()
```

## Grouped by category

```python
cerno.chart(df).kde("x", color="category").show()
```

## Histogram overlay

Pass a `cerno.kde()` config to the `kde` parameter of `.histogram()` to
overlay a density curve on top of the histogram. The curve is automatically
scaled to match the histogram's y-axis.

```python
cerno.chart(df).histogram("income", kde=cerno.kde()).show()

# Filled overlay
cerno.chart(df).histogram("income", kde=cerno.kde(fill=True, alpha=0.3)).show()
```

## Bandwidth

The `bw_method` parameter is passed to `scipy.stats.gaussian_kde`.

```python
cerno.chart(df).kde("x", bw_method=0.3).show()
```

## API reference

See {py:func}`cerno.kde`, {py:class}`cerno.stats.kde.KDE`,
and {py:meth}`cerno.core.chart.Chart.kde`.
