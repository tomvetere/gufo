# Line

A line chart connects data points in sequence. Use it for time series and
ordered data.

```python
cerno.chart(df).line("year", "revenue").show()
```

## Multiple series — wide-form data

Pass a list of column names as `y` to plot multiple series from a wide
DataFrame. No `pd.melt()` required.

```python
wide_df = pd.DataFrame({
    "year":      [2020, 2021, 2022, 2023],
    "product_a": [100,  130,  160,  210],
    "product_b": [80,   95,   115,  140],
    "product_c": [60,   70,   90,   125],
})

cerno.chart(wide_df).line("year", ["product_a", "product_b", "product_c"]).legend().show()
```

## Multiple series — long-form data

For long-form DataFrames, use `color` to group by a categorical column.

```python
cerno.chart(long_df).line("year", "revenue", color="product").legend().show()
```

## Continuous color

Pass a numeric column as `color` to draw a gradient line whose segments are
colored by the variable. An automatic colorbar is added.

```python
cerno.chart(df).line("x", "y", color="speed", cmap="viridis").show()

# Custom range and no colorbar
cerno.chart(df).line("x", "y", color="speed", vmin=0, vmax=100,
                     colorbar=False).show()
```

## Error band

Pass `y_error` (column name or array) to draw error bars or a confidence band
along the line.

```python
cerno.chart(df).line("year", "revenue", y_error="revenue_std").show()
```

## Data labels

Use `.label()` to annotate each point with its y-value or a column.

```python
cerno.chart(df).line("month", "revenue").label(fmt=".0f").show()
cerno.chart(df).line("month", "revenue").label("note").show()
```

## Line style

```python
cerno.chart(df).line("year", "forecast", stroke_dash="dashed").show()
```

Available values for `stroke_dash`: `"solid"` (default), `"dashed"`, `"dotted"`, `"dashdot"`.

## Layering with scatter

```python
(
    cerno.chart(df)
    .scatter("x", "y", alpha=0.5, label="Observations")
    .line("x", "trend", color="#333333", stroke_dash="dashed", label="Trend")
    .legend()
    .show()
)
```

## API reference

See {py:meth}`cerno.core.chart.Chart.line`.
