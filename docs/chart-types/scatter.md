# Scatter

A scatter plot shows the relationship between two numeric variables.

```python
cerno.chart(df).scatter("x", "y").show()
```

## Color encoding

Pass a column name to `color` to encode a categorical or numeric variable as
color. Cerno detects the type and handles discrete vs continuous coloring
automatically.

```python
# Categorical: one color per category, auto-legend entries
cerno.chart(df).scatter("x", "y", color="continent").legend().show()
```

## Size encoding

Pass a numeric column to `size` to encode a third variable as point area.
Values are normalized to a readable range automatically.

```python
cerno.chart(df).scatter("x", "y", size="population").show()

# Color and size together
cerno.chart(df).scatter(
    "gdp_per_capita", "life_expectancy",
    color="continent",
    size="population",
).legend().show()
```

## Transparency

Use `alpha` for dense data where overplotting is a problem.

```python
cerno.chart(df).scatter("x", "y", alpha=0.3).show()
```

## Regression overlay

Pass a `cerno.regression()` config to the `fit` parameter to add a fit line.

```python
cerno.chart(df).scatter("x", "y", fit=cerno.regression()).show()

# Polynomial fit
cerno.chart(df).scatter("x", "y", fit=cerno.regression(degree=2)).show()

# Custom styling
cerno.chart(df).scatter(
    "x", "y",
    fit=cerno.regression(color="red", linestyle="--", linewidth=3),
).show()
```

See [Regression overlay](regression.md) for full details.

## API reference

See {py:meth}`cerno.core.chart.Chart.scatter`.
