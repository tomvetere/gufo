"""Violin mark."""
from ..core.validate import check_array_lengths, warn_nan_inf
from ._base import apply_label, default_colors, group_by_x, is_wide_form, resolve_color


def render(layer, adapter, axes):
    enc = layer.encodings

    if is_wide_form(layer.y):
        _render_wide_form(layer, adapter, axes, enc)
        return

    x = adapter.resolve(layer.x)
    y = adapter.resolve(layer.y)
    kwargs = dict(layer.kwargs)

    check_array_lengths({"x": x, "y": y}, "violin")
    warn_nan_inf(y, "y", "violin")

    unique_x, grouped, positions = group_by_x(x, y)

    kwargs.setdefault("showmedians", True)

    horizontal = enc.get("horizontal")
    if horizontal:
        kwargs["orientation"] = "horizontal"

    apply_label(kwargs, enc)

    vp = axes.violinplot(grouped, positions=positions, **kwargs)

    color = resolve_color(adapter, enc.get("color"))
    _apply_body_colors(vp["bodies"], color)

    if horizontal:
        axes.set_yticks(positions, labels=unique_x)
    else:
        axes.set_xticks(positions, labels=unique_x)


def _render_wide_form(layer, adapter, axes, enc):
    series = adapter.resolve(layer.y)
    positions = list(range(1, len(layer.y) + 1))
    kwargs = dict(layer.kwargs)

    kwargs.setdefault("showmedians", True)

    horizontal = enc.get("horizontal")
    if horizontal:
        kwargs["orientation"] = "horizontal"

    apply_label(kwargs, enc)

    vp = axes.violinplot(series, positions=positions, **kwargs)

    color = resolve_color(adapter, enc.get("color"))
    _apply_body_colors(vp["bodies"], color)

    if horizontal:
        axes.set_yticks(positions, labels=layer.y)
    else:
        axes.set_xticks(positions, labels=layer.y)


def _apply_body_colors(bodies, color=None):
    """Apply color to violin bodies — single literal or distinct palette."""
    if color is not None and isinstance(color, str):
        colors = [color] * len(bodies)
    else:
        colors = default_colors(len(bodies))
    for body, c in zip(bodies, colors):
        body.set_facecolor(c)
        body.set_alpha(0.7)
