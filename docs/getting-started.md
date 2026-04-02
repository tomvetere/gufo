# Getting started

## Installation

```bash
pip install cerno
```

For the latest development version:

```bash
pip install git+https://github.com/thomas/cerno.git
```

## Your first chart

```python
import cerno
import pandas as pd

df = pd.read_csv("gapminder.csv")

cerno.chart(df).scatter("gdp_per_capita", "life_expectancy").show()
```

## The pattern

Every cerno chart follows the same structure:

1. **Create a chart** with `cerno.chart(data)` — pass your data once here.
2. **Add marks** — `.scatter()`, `.line()`, `.bar()`, `.histogram()`.
3. **Describe the chart** — `.title()`, `.xlabel()`, `.ylabel()`, `.legend()`.
4. **Output** — `.show()` to display, `.save("file.png")` to write to disk.

```python
(
    cerno.chart(df)
    .scatter("x", "y", color="category")   # mark
    .title("My Chart")                      # description
    .xlabel("X axis")
    .ylabel("Y axis")
    .legend()
    .show()                                 # output
)
```

Methods can be called in any order. `.show()` and `.save()` trigger rendering —
everything before them just registers intent.

## What data cerno accepts

You do not need to reshape your data before passing it in:

- **pandas DataFrame** — long-form or wide-form, refer to columns by name
- **dict** — `{"x": [...], "y": [...]}`
- **numpy arrays or lists** — pass directly to mark methods, omit data from `cerno.chart()`

See [Data formats](guides/data-formats.md) for details and examples.

## Running the tests

If you are contributing or want to verify your installation:

```bash
pip install pytest
pytest tests/ -v
```

## Next steps

- [Chart types](chart-types/index.md) — examples for every mark
- [Theming](guides/theming.md) — built-in themes and custom theme creation
- [API reference](api/index.md) — full method documentation
