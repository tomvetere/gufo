"""Box plot mark."""
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

    check_array_lengths({"x": x, "y": y}, "boxplot")
    warn_nan_inf(y, "y", "boxplot")

    unique_x, grouped, _ = group_by_x(x, y)

    kwargs["patch_artist"] = True
    kwargs["tick_labels"] = unique_x

    if enc.get("horizontal"):
        kwargs["orientation"] = "horizontal"

    color = resolve_color(adapter, enc.get("color"))
    if color is not None and isinstance(color, str):
        kwargs.setdefault("boxprops", {})["facecolor"] = color
        kwargs.setdefault("medianprops", {})["color"] = "black"

    apply_label(kwargs, enc)

    axes.boxplot(grouped, **kwargs)


def _render_wide_form(layer, adapter, axes, enc):
    series = adapter.resolve(layer.y)
    kwargs = dict(layer.kwargs)

    kwargs["patch_artist"] = True
    kwargs["tick_labels"] = layer.y

    if enc.get("horizontal"):
        kwargs["orientation"] = "horizontal"

    apply_label(kwargs, enc)

    bp = axes.boxplot(series, **kwargs)

    colors = default_colors(len(layer.y))
    for box, color in zip(bp["boxes"], colors):
        box.set_facecolor(color)
