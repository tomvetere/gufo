# Theming

Gufo ships three built-in themes and a composable system for creating custom themes.

## Built-in themes

| Name | Description |
|------|-------------|
| `gufo_modern` | Default. Light gray axes background, no spines, white grid lines. |
| `gufo_dark` | Dark navy background. Suited for dark-mode notebooks and presentations. |
| `gufo_print` | White background, serif font, grayscale palette. Print and publication safe. |

## Set a global theme

Applies to all charts created after the call.

```python
import gufo

gufo.set_theme("gufo_dark")

# All subsequent charts use the dark theme
gufo.chart(df).scatter("x", "y").show()
```

Reset to the default at any time:

```python
gufo.set_theme("gufo_modern")
```

## Per-chart theme

Apply a theme to one chart without affecting global state.

```python
gufo.chart(df).theme("gufo_dark").scatter("x", "y").show()
```

## Temporary theme with a context manager

Use `gufo.theme_context()` to scope a theme to a block of code.

```python
with gufo.theme_context("gufo_print"):
    gufo.chart(df).scatter("x", "y").save("print_ready.pdf")

# Global theme is unchanged after the block exits
```

## Custom themes

Themes are immutable objects. Create a new theme by merging overrides onto an
existing one, then registering it by name.

```python
my_theme = (
    gufo.get_theme("gufo_modern")
    .merge({
        "axes.facecolor": "#1a1a2e",
        "figure.facecolor": "#16213e",
    })
    .rename("brand_dark")
)

gufo.register_theme(my_theme)
gufo.set_theme("brand_dark")
```

`merge()` returns a new `Theme` — the original is not modified.

Any matplotlib rcParam key is valid in `merge()`. See the
[matplotlib rcParams reference](https://matplotlib.org/stable/users/explain/customizing.html)
for the full list of available keys.

## API reference

See {py:mod}`gufo.style.theme`.
