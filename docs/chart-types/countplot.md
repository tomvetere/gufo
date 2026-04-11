# Count plot

A count plot shows the frequency of each category as bars — like a
histogram for categorical data.

```python
cerno.chart(df).countplot("animal").show()
```

## Horizontal

```python
cerno.chart(df).countplot("animal", horizontal=True).show()
```

## Color

Group bars by a second categorical column.

```python
cerno.chart(df).countplot("animal", color="owner").legend().show()
```

## API reference

See {py:meth}`cerno.core.chart.Chart.countplot`.
