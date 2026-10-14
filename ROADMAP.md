# Roadmap

Planned work for upcoming gufo releases. Plans can change; released versions are recorded in [`CHANGELOG.md`](CHANGELOG.md).

- **v0.3.0**: mixin decomposition — split Chart into MarksMixin, DecoratorsMixin, AxisMixin, ReferenceMixin for maintainability (no public API changes); plan introspection (`.explain()` — print the deferred plan without rendering; design not yet settled)
- **v0.4.0**: 2D KDE/contour (bivariate `.kdeplot("x", "y")`), ridgeline plot
- **v0.5.0**: built-in aggregation (`agg=` on bar/line/pointplot), confidence bands on line (`ci=`)
- **v0.6.0**: secondary y-axis (`.twin_y()`), pattern fills (`hatch=` on bar/histogram/area)
- **v0.7.0**: notebook auto-repr (`_repr_png_`), stricter type hints (`py.typed`, Literal types)
- **v1.0.0**: stable API — plugin system for custom marks, theme gallery

Patch releases (v0.x.y) ship between minor versions as needed for bug fixes.
