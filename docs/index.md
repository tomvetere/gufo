# gufo

**Data visualization simplified.**

Gufo is a Python library for making charts — built on matplotlib, designed so
you can explore and present data without fighting your tools.

```python
import gufo

(
    gufo.chart(df)
    .scatter("gdp_per_capita", "life_expectancy", color="continent", size="population")
    .title("GDP vs Life Expectancy")
    .xlabel("GDP per Capita (USD)")
    .ylabel("Life Expectancy (years)")
    .legend()
    .save("output.png")
)
```

## Install

```bash
pip install gufo
```

## Core idea

Everything goes through `gufo.chart(data)`. You chain methods to describe
what you want. Nothing is drawn until you call `.show()` or `.save()`.

```{toctree}
:maxdepth: 1
:caption: Getting started

getting-started
gallery
```

```{toctree}
:maxdepth: 2
:caption: Chart types

chart-types/index
```

```{toctree}
:maxdepth: 2
:caption: Guides

guides/data-formats
guides/theming
guides/layout
guides/pairplot
guides/matplotlib-escape-hatch
```

```{toctree}
:maxdepth: 2
:caption: API reference

api/index
```

```{toctree}
:maxdepth: 1
:caption: Project

architecture
changelog
```
