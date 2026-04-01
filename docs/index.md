# cerno

**Data visualization for humans.**

Cerno is a Python library for making charts — built on matplotlib, designed so
you can explore and present data without fighting your tools.

```python
import cerno

(
    cerno.chart(df)
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
pip install cerno
```

## Core idea

Everything goes through `cerno.chart(data)`. You chain methods to describe
what you want. Nothing is drawn until you call `.show()` or `.save()`.

```{toctree}
:maxdepth: 1
:caption: Getting started

getting-started
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

changelog
```
