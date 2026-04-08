# Layout

## Grid

The `Grid` class is a standalone layout container for arranging multiple charts
in a rows x cols grid. Users create instances via `cerno.grid()`, never by
instantiating `Grid` directly.

### Entry point

```python
g = cerno.grid(rows=2, cols=2, figsize=(14, 10))
```

### Key methods

- `Grid.__setitem__(idx, panel_chart)` — assign a `Chart` to a grid cell
- `Grid.title(text)` — set a super-title above all panels
- `Grid.theme(name_or_theme)` — set a grid-level theme
- `Grid.apply(func)` — call `func(figure, axes_2d_array)` after rendering
- `Grid.show()` — render and display the grid
- `Grid.save(path, *, dpi=150)` — render and save to file
