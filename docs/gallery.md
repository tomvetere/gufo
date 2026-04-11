# Gallery

A visual overview of every chart type cerno supports. Each example uses
synthetic data and can be copy-pasted as a starting point.

## Scatter

```python
cerno.chart(df).scatter("x", "y", color="category", size="size").show()
```

```{image} _static/gallery/scatter.png
:width: 600px
```

## Scatter — continuous color

```python
cerno.chart(df).scatter("x", "y", color="value", cmap="viridis").show()
```

```{image} _static/gallery/scatter_continuous.png
:width: 600px
```

## Line

```python
cerno.chart(df).line("day", "sales", color="channel").legend().show()
```

```{image} _static/gallery/line.png
:width: 600px
```

## Bar — grouped

```python
cerno.chart(df).bar("fruit", "count", color="region").show()
```

```{image} _static/gallery/bar_grouped.png
:width: 600px
```

## Bar — stacked

```python
cerno.chart(df).bar("fruit", "count", color="region", stacked=True).show()
```

```{image} _static/gallery/bar_stacked.png
:width: 600px
```

## Histogram with KDE

```python
cerno.chart(df).histogram("x", kde=cerno.kde()).show()
```

```{image} _static/gallery/histogram_kde.png
:width: 600px
```

## Box plot

```python
cerno.chart(df).boxplot("group", "value", color="sub").show()
```

```{image} _static/gallery/boxplot.png
:width: 600px
```

## Violin

```python
cerno.chart(df).violin("group", "value", color="sub").show()
```

```{image} _static/gallery/violin.png
:width: 600px
```

## Heatmap

```python
cerno.chart(pivot_df).heatmap(annotate=True, cmap="YlOrRd").show()
```

```{image} _static/gallery/heatmap.png
:width: 600px
```

## Area — stacked

```python
cerno.chart(df).area("month", ["product_a", "product_b", "product_c"]).show()
```

```{image} _static/gallery/area.png
:width: 600px
```

## KDE — filled density

```python
cerno.chart(df).kde("x", fill=True, color="category").show()
```

```{image} _static/gallery/kde.png
:width: 600px
```

## Strip plot

```python
cerno.chart(df).strip("group", "value", color="sub", alpha=0.6).show()
```

```{image} _static/gallery/strip.png
:width: 600px
```

## Swarm plot

```python
cerno.chart(df).swarm("group", "value", alpha=0.6).show()
```

```{image} _static/gallery/swarm.png
:width: 600px
```

## Count plot

```python
cerno.chart(df).countplot("animal", color="owner").show()
```

```{image} _static/gallery/countplot.png
:width: 600px
```

## ECDF

```python
cerno.chart(df).ecdf("x", color="category").show()
```

```{image} _static/gallery/ecdf.png
:width: 600px
```

## Histogram + rug plot

```python
cerno.chart(df).histogram("x").rug("x", color="red").show()
```

```{image} _static/gallery/rug.png
:width: 600px
```

## Pair plot

```python
cerno.pairplot(df, ["a", "b", "c"], color="species").show()
```

```{image} _static/gallery/pairplot.png
:width: 600px
```

## Joint plot

```python
cerno.jointplot(df, "x", "y").show()
```

```{image} _static/gallery/jointplot.png
:width: 600px
```

## Faceted scatter

```python
cerno.chart(df).scatter("x", "y").facet("category").show()
```

```{image} _static/gallery/faceted.png
:width: 600px
```
