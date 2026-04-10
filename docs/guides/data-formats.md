# Data formats

Cerno accepts data in several formats and resolves them transparently. You
never need to convert your data before passing it in.

## pandas DataFrame

The most common case. Pass the DataFrame to `cerno.chart()`, then refer to
columns by name.

```python
import cerno
import pandas as pd

df = pd.read_csv("data.csv")
cerno.chart(df).scatter("x", "y").show()
```

### Long-form DataFrames

Long-form (tidy) data has one row per observation. Group by a column using
`color=`.

```python
cerno.chart(long_df).line("year", "revenue", color="product").legend().show()
```

### Wide-form DataFrames

Wide-form data works without reshaping. Pass a list of column names as `y`.

```python
wide_df = pd.DataFrame({
    "month": ["Jan", "Feb", "Mar", "Apr"],
    "north": [120, 135, 118, 142],
    "south": [98,  102, 110, 107],
    "east":  [85,  91,  88,  96],
})

cerno.chart(wide_df).line("month", ["north", "south", "east"]).legend().show()
```

## Polars DataFrame

Polars works exactly like pandas — pass a Polars DataFrame to `cerno.chart()`
and refer to columns by name.

```python
import polars as pl

df = pl.read_csv("data.csv")
cerno.chart(df).scatter("x", "y").show()
```

Install with `pip install cerno[polars]`.

## dict

Pass a plain Python dict. Keys become column names.

```python
cerno.chart({"x": [1, 2, 3], "y": [4, 5, 6]}).scatter("x", "y").show()
```

## Arrays and lists

When your data is already in arrays or lists, omit the data argument entirely
and pass the arrays directly to the mark method.

```python
import numpy as np

xs = np.arange(100)
ys = np.random.cumsum(np.random.randn(100))

cerno.chart().line(xs, ys).show()
cerno.chart().scatter([1, 2, 3], [4, 5, 6]).show()
```

## Mixing arrays and column names

You can overlay a computed series on a DataFrame-backed chart by passing arrays
directly to a second mark.

```python
import numpy as np

# Fit a trend line to data in the DataFrame
trend = np.polyval(np.polyfit(df["x"], df["y"], 1), df["x"])

(
    cerno.chart(df)
    .scatter("x", "y", alpha=0.5, label="Data")
    .line(df["x"].values, trend, color="red", label="Trend")
    .legend()
    .show()
)
```
