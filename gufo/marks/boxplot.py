"""Box plot mark."""
import numpy as np

from ..core.validate import check_array_lengths, warn_nan_inf
from ._base import (
    _resolve_order, apply_label, default_colors, group_by_x, is_wide_form,
    iter_color_groups, resolve_color,
)


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

    color_value = resolve_color(adapter, enc.get("color"))
    groups = iter_color_groups(color_value, palette=layer.palette,
                               color_order=enc.get("color_order"))

    if groups is not None:
        _render_grouped(x, y, color_value, groups, axes, enc, kwargs)
        return

    unique_x, grouped, _ = group_by_x(x, y, order=enc.get("order"))

    kwargs["patch_artist"] = True
    kwargs["tick_labels"] = unique_x

    if enc.get("horizontal"):
        kwargs["orientation"] = "horizontal"

    if color_value is not None and isinstance(color_value, str):
        kwargs.setdefault("boxprops", {})["facecolor"] = color_value
        kwargs.setdefault("medianprops", {})["color"] = "black"

    apply_label(kwargs, enc)

    axes.boxplot(grouped, **kwargs)


def _render_grouped(x, y, color_value, groups, axes, enc, extra_kwargs):
    """Render side-by-side grouped boxes for categorical color."""
    x = np.asarray(x)
    y = np.asarray(y, dtype=float)
    color_value = np.asarray(color_value)

    unique_x = _resolve_order(x, enc.get("order"))
    n_colors = len(groups)
    sub_width = 0.6 / n_colors
    horizontal = enc.get("horizontal", False)

    for i, (cat, color, _) in enumerate(groups):
        data = []
        positions = []
        for j, x_val in enumerate(unique_x):
            mask = (x == x_val) & (color_value == cat)
            data.append(y[mask])
            base = j + 1
            positions.append(base + (i - n_colors / 2 + 0.5) * sub_width)

        kwargs = dict(extra_kwargs, patch_artist=True,
                      widths=sub_width * 0.8, manage_ticks=False)
        kwargs.setdefault("medianprops", {})["color"] = "black"
        if horizontal:
            kwargs["orientation"] = "horizontal"

        bp = axes.boxplot(data, positions=positions, **kwargs)
        for box in bp["boxes"]:
            box.set_facecolor(color)

        axes.plot([], [], color=color, label=cat, linewidth=6)

    tick_positions = list(range(1, len(unique_x) + 1))
    if horizontal:
        axes.set_yticks(tick_positions, labels=unique_x)
    else:
        axes.set_xticks(tick_positions, labels=unique_x)


def _render_wide_form(layer, adapter, axes, enc):
    series = adapter.resolve(layer.y)
    kwargs = dict(layer.kwargs)

    kwargs["patch_artist"] = True
    kwargs["tick_labels"] = layer.y

    if enc.get("horizontal"):
        kwargs["orientation"] = "horizontal"

    apply_label(kwargs, enc)

    bp = axes.boxplot(series, **kwargs)

    colors = default_colors(len(layer.y), palette=layer.palette)
    for box, color in zip(bp["boxes"], colors):
        box.set_facecolor(color)
