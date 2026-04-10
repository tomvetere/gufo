# Swarm plot

A swarm plot arranges individual data points along a categorical axis using a
beeswarm algorithm that avoids overlapping points. Requires scipy
(`pip install cerno[scipy]`).

```python
cerno.chart(df).swarm("department", "salary").show()
```

## Horizontal

```python
cerno.chart(df).swarm("department", "salary", horizontal=True).show()
```

## Color

```python
cerno.chart(df).swarm("department", "salary", color="coral").show()
```

## Wide-form data

Pass a list of column names as `y` to create one swarm per column.

```python
cerno.chart(df).swarm(None, ["q1_scores", "q2_scores", "q3_scores"]).show()
```

## API reference

See {py:meth}`cerno.core.chart.Chart.swarm`.
