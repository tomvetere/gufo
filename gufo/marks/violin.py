"""Violin mark."""
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

    check_array_lengths({"x": x, "y": y}, "violin")
    warn_nan_inf(y, "y", "violin")

    color_value = resolve_color(adapter, enc.get("color"))
    groups = iter_color_groups(color_value, palette=layer.palette,
                               color_order=enc.get("color_order"))

    if groups is not None:
        _render_grouped(x, y, color_value, groups, axes, enc, kwargs)
        return

    unique_x, grouped, positions = group_by_x(x, y, order=enc.get("order"))

    kwargs.setdefault("showmedians", True)

    horizontal = enc.get("horizontal")
    if horizontal:
        kwargs["orientation"] = "horizontal"

    apply_label(kwargs, enc)

    vp = axes.violinplot(grouped, positions=positions, **kwargs)

    _apply_body_colors(vp["bodies"], color_value, palette=layer.palette)

    if horizontal:
        axes.set_yticks(positions, labels=unique_x)
    else:
        axes.set_xticks(positions, labels=unique_x)


def _render_grouped(x, y, color_value, groups, axes, enc, extra_kwargs):
    """Render side-by-side grouped violins for categorical color."""
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
            subset = y[mask]
            if len(subset) < 2:
                continue
            data.append(subset)
            base = j + 1
            positions.append(base + (i - n_colors / 2 + 0.5) * sub_width)

        if not data:
            continue

        kwargs = dict(extra_kwargs, showmedians=True,
                      widths=sub_width * 0.8)
        if horizontal:
            kwargs["orientation"] = "horizontal"

        vp = axes.violinplot(data, positions=positions, **kwargs)
        for body in vp["bodies"]:
            body.set_facecolor(color)
            body.set_alpha(0.7)

        axes.plot([], [], color=color, label=cat, linewidth=6)

    tick_positions = list(range(1, len(unique_x) + 1))
    if horizontal:
        axes.set_yticks(tick_positions, labels=unique_x)
    else:
        axes.set_xticks(tick_positions, labels=unique_x)


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
    _apply_body_colors(vp["bodies"], color, palette=layer.palette)

    if horizontal:
        axes.set_yticks(positions, labels=layer.y)
    else:
        axes.set_xticks(positions, labels=layer.y)


def _apply_body_colors(bodies, color=None, palette=None):
    """Apply color to violin bodies — single literal or distinct palette."""
    if color is not None and isinstance(color, str):
        colors = [color] * len(bodies)
    else:
        colors = default_colors(len(bodies), palette=palette)
    for body, c in zip(bodies, colors):
        body.set_facecolor(c)
        body.set_alpha(0.7)
