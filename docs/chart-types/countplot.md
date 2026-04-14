# Count plot

A count plot shows the frequency of each category as bars — like a
histogram for categorical data.

```python
gufo.chart(df).countplot("animal").show()
```

## Horizontal

```python
gufo.chart(df).countplot("animal", horizontal=True).show()
```

## Color

Group bars by a second categorical column.

```python
gufo.chart(df).countplot("animal", color="owner").legend().show()
```

## API reference

See {py:meth}`gufo.core.chart.Chart.countplot`.
