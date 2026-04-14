# Histogram

A histogram shows the distribution of a numeric variable.

```python
gufo.chart(df).histogram("income").show()
```

## Bin count

```python
gufo.chart(df).histogram("income", bins=40).show()
```

The default is `"auto"`, which delegates to matplotlib's automatic bin selection
(Sturges' or Freedman-Diaconis estimator depending on data size).

## From a raw array

When your data is in a numpy array or list, omit the data argument from
`gufo.chart()` and pass the array directly.

```python
import numpy as np

data = np.random.normal(0, 1, 1000)
gufo.chart().histogram(data).show()
```

## KDE overlay

Pass a `gufo.kde()` config to overlay a density curve on the histogram.
The curve is automatically scaled to match the histogram's y-axis.
Requires scipy (`pip install gufo[scipy]`).

```python
gufo.chart(df).histogram("income", kde=gufo.kde()).show()

# Filled overlay
gufo.chart(df).histogram("income", kde=gufo.kde(fill=True, alpha=0.3)).show()
```

See [KDE](kde.md) for standalone density plots and full details.

## API reference

See {py:meth}`gufo.core.chart.Chart.histogram`.
