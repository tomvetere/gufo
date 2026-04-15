# Gallery

A visual overview of every chart type gufo supports. Each example uses
synthetic data and can be copy-pasted as a starting point.

## Scatter

```python
gufo.chart(df).scatter("x", "y", color="category", size="size").show()
```

```{image} _static/gallery/scatter.png
:width: 600px
```

## Scatter — continuous color

```python
gufo.chart(df).scatter("x", "y", color="value", cmap="viridis").show()
```

```{image} _static/gallery/scatter_continuous.png
:width: 600px
```

## Line

```python
gufo.chart(df).line("day", "sales", color="channel").legend().show()
```

```{image} _static/gallery/line.png
:width: 600px
```

## Bar — grouped

```python
gufo.chart(df).bar("fruit", "count", color="region").show()
```

```{image} _static/gallery/bar_grouped.png
:width: 600px
```

## Bar — stacked

```python
gufo.chart(df).bar("fruit", "count", color="region", stacked=True).show()
```

```{image} _static/gallery/bar_stacked.png
:width: 600px
```

## Histogram with KDE

```python
gufo.chart(df).histogram("x", kde=gufo.kde()).show()
```

```{image} _static/gallery/histogram_kde.png
:width: 600px
```

## Box plot

```python
gufo.chart(df).boxplot("group", "value", color="sub").show()
```

```{image} _static/gallery/boxplot.png
:width: 600px
```

## Violin

```python
gufo.chart(df).violin("group", "value", color="sub").show()
```

```{image} _static/gallery/violin.png
:width: 600px
```

## Heatmap

```python
gufo.chart(pivot_df).heatmap(annotate=True, cmap="YlOrRd").show()
```

```{image} _static/gallery/heatmap.png
:width: 600px
```

## Area — stacked

```python
gufo.chart(df).area("month", ["product_a", "product_b", "product_c"]).show()
```

```{image} _static/gallery/area.png
:width: 600px
```

## KDE — filled density

```python
gufo.chart(df).kdeplot("x", fill=True, color="category").show()
```

```{image} _static/gallery/kde.png
:width: 600px
```

## Strip plot

```python
gufo.chart(df).strip("group", "value", color="sub", alpha=0.6).show()
```

```{image} _static/gallery/strip.png
:width: 600px
```

## Swarm plot

```python
gufo.chart(df).swarm("group", "value", alpha=0.6).show()
```

```{image} _static/gallery/swarm.png
:width: 600px
```

## Count plot

```python
gufo.chart(df).countplot("animal", color="owner").show()
```

```{image} _static/gallery/countplot.png
:width: 600px
```

## ECDF

```python
gufo.chart(df).ecdf("x", color="category").show()
```

```{image} _static/gallery/ecdf.png
:width: 600px
```

## Histogram + rug plot

```python
gufo.chart(df).histogram("x").rug("x", color="red").show()
```

```{image} _static/gallery/rug.png
:width: 600px
```

## Pair plot

```python
gufo.pairplot(df, ["a", "b", "c"], color="species").show()
```

```{image} _static/gallery/pairplot.png
:width: 600px
```

## Joint plot

```python
gufo.jointplot(df, "x", "y").show()
```

```{image} _static/gallery/jointplot.png
:width: 600px
```

## Faceted scatter

```python
gufo.chart(df).scatter("x", "y").facet("category").show()
```

```{image} _static/gallery/faceted.png
:width: 600px
```
