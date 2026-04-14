# The matplotlib escape hatch

Gufo covers the most common chart types and customizations. For everything
else, `.apply()` gives you direct access to the underlying matplotlib
`Figure` and `Axes` without leaving the chain.

## Basic usage

```python
(
    gufo.chart(df)
    .line("year", "gdp")
    .apply(lambda fig, ax: ax.axvspan(2008, 2009, alpha=0.15, color="gray"))
    .title("GDP with Recession Band")
    .show()
)
```

The function receives `(figure, axes)` and its return value is ignored. The
`Chart` is returned so further method calls work normally.

## Named functions

For anything more than a one-liner, use a named function.

```python
def add_recession_bands(fig, ax):
    recessions = [(2001, 2001), (2008, 2009), (2020, 2020)]
    for start, end in recessions:
        ax.axvspan(start, end, alpha=0.15, color="gray")

gufo.chart(df).line("year", "gdp").apply(add_recession_bands).show()
```

## Order of execution

`.apply()` functions run after all layers and decorators are rendered:

1. Theme is applied
2. Figure and axes are created
3. All mark layers are drawn (`.scatter()`, `.line()`, etc.)
4. Decorators are applied (`.title()`, `.xlabel()`, axis limits, legend)
5. Each `.apply()` function runs in registration order

This means `.apply()` has full access to the final, decorated chart.

## Multiple apply calls

You can chain multiple `.apply()` calls. They run in the order registered.

```python
(
    gufo.chart(df)
    .line("year", "gdp")
    .apply(add_recession_bands)
    .apply(lambda fig, ax: ax.axhline(0, color="black", linewidth=0.8))
    .show()
)
```

## When to use it

Good candidates for `.apply()`:

- Reference lines and bands (`axhline`, `axvline`, `axvspan`, `axhspan`)
- Custom annotations beyond what `.annotate()` supports
- `fill_between` for shaded regions
- Error bars (`errorbar`)
- Any specialized matplotlib feature not yet in gufo

If you find yourself using `.apply()` for the same pattern repeatedly,
[open an issue](https://github.com/tomvetere/gufo/issues) — it is a candidate
for a native gufo feature.

## API reference

See {py:meth}`gufo.core.chart.Chart.apply`.
