# Scatter

A scatter plot shows the relationship between two numeric variables.

```python
gufo.chart(df).scatter("x", "y").show()
```

## Color encoding

Pass a column name to `color` to encode a categorical or numeric variable as
color. Gufo detects the type and handles discrete vs continuous coloring
automatically.

```python
# Categorical: one color per category, auto-legend entries
gufo.chart(df).scatter("x", "y", color="continent").legend().show()
```

## Size encoding

Pass a numeric column to `size` to encode a third variable as point area.
Values are normalized to a readable range automatically.

```python
gufo.chart(df).scatter("x", "y", size="population").show()

# Color and size together
gufo.chart(df).scatter(
    "gdp_per_capita", "life_expectancy",
    color="continent",
    size="population",
).legend().show()
```

## Transparency

Use `alpha` for dense data where overplotting is a problem.

```python
gufo.chart(df).scatter("x", "y", alpha=0.3).show()
```

## Regression overlay

Pass a `gufo.regression()` config to the `fit` parameter to add a fit line.

```python
gufo.chart(df).scatter("x", "y", fit=gufo.regression()).show()

# Polynomial fit
gufo.chart(df).scatter("x", "y", fit=gufo.regression(degree=2)).show()

# Custom styling
gufo.chart(df).scatter(
    "x", "y",
    fit=gufo.regression(color="red", linestyle="--", linewidth=3),
).show()
```

See [Regression overlay](regression.md) for full details.

## LOWESS smoothing

Pass a `gufo.lowess()` config to the `fit` parameter for a non-parametric smooth.
Requires statsmodels (`pip install gufo[stats]`).

```python
gufo.chart(df).scatter("x", "y", fit=gufo.lowess()).show()

# Custom smoothing fraction (lower = more wiggly)
gufo.chart(df).scatter("x", "y", fit=gufo.lowess(frac=0.3)).show()
```

## Data labels

Label each point with values from a column.

```python
gufo.chart(df).scatter("x", "y").label("name").show()
```

## API reference

See {py:meth}`gufo.core.chart.Chart.scatter`.
