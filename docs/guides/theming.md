# Theming

Cerno ships three built-in themes and a composable system for creating custom themes.

## Built-in themes

| Name | Description |
|------|-------------|
| `cerno_modern` | Default. Light gray axes background, no spines, white grid lines. |
| `cerno_dark` | Dark navy background. Suited for dark-mode notebooks and presentations. |
| `cerno_print` | White background, serif font, grayscale palette. Print and publication safe. |

## Set a global theme

Applies to all charts created after the call.

```python
import cerno

cerno.set_theme("cerno_dark")

# All subsequent charts use the dark theme
cerno.chart(df).scatter("x", "y").show()
```

Reset to the default at any time:

```python
cerno.set_theme("cerno_modern")
```

## Per-chart theme

Apply a theme to one chart without affecting global state.

```python
cerno.chart(df).theme("cerno_dark").scatter("x", "y").show()
```

## Temporary theme with a context manager

Use `cerno.theme_context()` to scope a theme to a block of code.

```python
with cerno.theme_context("cerno_print"):
    cerno.chart(df).scatter("x", "y").save("print_ready.pdf")

# Global theme is unchanged after the block exits
```

## Custom themes

Themes are immutable objects. Create a new theme by merging overrides onto an
existing one, then registering it by name.

```python
my_theme = (
    cerno.get_theme("cerno_modern")
    .merge({
        "axes.facecolor": "#1a1a2e",
        "figure.facecolor": "#16213e",
    })
    .rename("brand_dark")
)

cerno.register_theme(my_theme)
cerno.set_theme("brand_dark")
```

`merge()` returns a new `Theme` — the original is not modified.

Any matplotlib rcParam key is valid in `merge()`. See the
[matplotlib rcParams reference](https://matplotlib.org/stable/users/explain/customizing.html)
for the full list of available keys.

## API reference

See {py:mod}`cerno.style.theme`.
