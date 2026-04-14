# Rug plot

A rug plot draws small tick marks along the x-axis to show individual
observations. It works well layered with a histogram or KDE.

```python
gufo.chart(df).rug("income").show()
```

## Customize height and opacity

```python
gufo.chart(df).rug("income", height=0.1, alpha=0.8).show()
```

## Color

```python
gufo.chart(df).rug("income", color="region").legend().show()
```

## Layered with histogram

```python
gufo.chart(df).histogram("income").rug("income", color="red").show()
```

## API reference

See {py:meth}`gufo.core.chart.Chart.rug`.
