# Heatmap

A heatmap visualizes a matrix of values as colored cells.

## Matrix form

When the DataFrame itself is the matrix, call `.heatmap()` with no arguments.

```python
gufo.chart(pivot_df).heatmap().show()
```

## Long-form

When data is in long-form columns, specify `x`, `y`, and `color`. Gufo pivots
internally.

```python
gufo.chart(df).heatmap("x_col", "y_col", color="value").show()
```

## Custom colormap

```python
gufo.chart(pivot_df).heatmap(cmap="coolwarm").show()
```

## Cell annotations

```python
gufo.chart(pivot_df).heatmap(annotate=True).show()
```

## API reference

See {py:meth}`gufo.core.chart.Chart.heatmap`.
