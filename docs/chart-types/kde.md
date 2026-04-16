# KDE (kernel density estimation)

A KDE plot shows the estimated probability density of a numeric variable.
Requires scipy (`pip install gufo[scipy]`).

## Standalone density plot

```python
gufo.chart(df).kdeplot("x").show()
```

## Filled density

```python
gufo.chart(df).kdeplot("x", fill=True).show()
```

## Grouped by category

```python
gufo.chart(df).kdeplot("x", color="category").show()
```

## Histogram overlay

Pass a `gufo.kde()` config to the `kde` parameter of `.histogram()` to
overlay a density curve on top of the histogram. The curve is automatically
scaled to match the histogram's y-axis.

```python
gufo.chart(df).histogram("income", kde=gufo.kde()).show()

# Filled overlay
gufo.chart(df).histogram("income", kde=gufo.kde(fill=True, alpha=0.3)).show()
```

## Bandwidth

The `bw_method` parameter is passed to `scipy.stats.gaussian_kde`.

```python
gufo.chart(df).kdeplot("x", bw_method=0.3).show()
```

## Matplotlib passthrough

Extra keyword arguments are forwarded to the underlying `axes.plot()` or
`axes.fill_between()` call.

```python
gufo.chart(df).kdeplot("x", zorder=5, dash_capstyle="round").show()
```

## API reference

See {py:func}`gufo.kde`, {py:class}`gufo.stats.kde.KDE`,
and {py:meth}`gufo.core.chart.Chart.kdeplot`.
