# Histogram

A histogram shows the distribution of a numeric variable.

```python
cerno.chart(df).histogram("income").show()
```

## Bin count

```python
cerno.chart(df).histogram("income", bins=40).show()
```

The default is `"auto"`, which delegates to matplotlib's automatic bin selection
(Sturges' or Freedman-Diaconis estimator depending on data size).

## From a raw array

When your data is in a numpy array or list, omit the data argument from
`cerno.chart()` and pass the array directly.

```python
import numpy as np

data = np.random.normal(0, 1, 1000)
cerno.chart().histogram(data).show()
```

## API reference

See {py:meth}`cerno.core.chart.Chart.histogram`.
