# Pair plot

A pair plot shows scatter plots for every pair of numeric columns, with
histograms along the diagonal. Useful for quickly exploring relationships
across multiple variables.

```python
cerno.pairplot(df).show()
```

## Color by category

```python
cerno.pairplot(df, color="species").show()
```

## Column subset

By default, all numeric columns are included. Use `columns` to limit which
variables appear.

```python
cerno.pairplot(df, columns=["sepal_length", "sepal_width", "petal_length"]).show()
```

## Saving and customization

`pairplot()` returns a `Grid`, so all grid methods work:

```python
cerno.pairplot(df, color="species").title("Iris Dataset").save("pairs.png", dpi=300)
```

## API reference

```{eval-rst}
.. autofunction:: cerno.layout.pairplot.pairplot
```
