"""Area mark."""
from ..core.validate import check_array_lengths, warn_nan_inf
from ._base import (
    apply_label, apply_color, default_colors, is_wide_form,
    resolve_color, iter_color_groups,
)


def render(layer, adapter, axes):
    enc = layer.encodings

    if is_wide_form(layer.y):
        _render_wide_form(layer, adapter, axes, enc)
        return

    x = adapter.resolve(layer.x)
    y = adapter.resolve(layer.y)
    kwargs = dict(layer.kwargs)

    check_array_lengths({"x": x, "y": y}, "area")
    warn_nan_inf(y, "y", "area")

    kwargs.setdefault("alpha", enc.get("alpha", 0.7))

    color_enc = enc.get("color")
    color_value = resolve_color(adapter, color_enc)
    groups = iter_color_groups(color_value)

    if groups is not None:
        for cat, color, mask in groups:
            axes.fill_between(x[mask], y[mask], color=color, label=cat, **kwargs)
        return

    apply_label(kwargs, enc)
    apply_color(kwargs, adapter, enc)

    axes.fill_between(x, y, **kwargs)


def _render_wide_form(layer, adapter, axes, enc):
    """Render wide-form data as a stacked area chart."""
    x = adapter.resolve(layer.x)
    series = adapter.resolve(layer.y)

    if series and len(series[0]) != len(x):
        check_array_lengths({"x": x, layer.y[0]: series[0]}, "area")

    kwargs = dict(layer.kwargs)
    kwargs.setdefault("alpha", enc.get("alpha", 0.7))
    colors = default_colors(len(layer.y))

    axes.stackplot(x, *series, labels=layer.y, colors=colors, **kwargs)
