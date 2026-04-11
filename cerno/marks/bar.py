"""Bar mark."""
import numpy as np

from ..core.validate import check_array_lengths, warn_nan_inf
from ._base import (
    apply_label, apply_color, default_colors, is_wide_form,
    resolve_color, resolve_errors, iter_color_groups,
)


def render(layer, adapter, axes):
    enc = layer.encodings

    if is_wide_form(layer.y):
        _render_wide_form(layer, adapter, axes, enc)
        return

    x = adapter.resolve(layer.x)
    y = adapter.resolve(layer.y)

    color_value = resolve_color(adapter, enc.get("color"))
    groups = iter_color_groups(color_value, palette=layer.palette)

    if groups is not None:
        _render_color_groups(x, y, groups, axes, enc, layer.kwargs)
        return

    kwargs = dict(layer.kwargs)

    check_array_lengths({"x": x, "y": y}, "bar")
    warn_nan_inf(y, "y", "bar")

    apply_label(kwargs, enc)
    apply_color(kwargs, adapter, enc)

    yerr, xerr = resolve_errors(adapter, enc)
    if yerr is not None:
        kwargs["yerr"] = yerr
    if xerr is not None:
        kwargs["xerr"] = xerr

    if enc.get("horizontal"):
        axes.barh(x, y, **kwargs)
    else:
        axes.bar(x, y, **kwargs)


def _render_color_groups(x, y, groups, axes, enc, extra_kwargs):
    """Render dodged or stacked bars grouped by a categorical color column."""
    x = np.asarray(x)
    y = np.asarray(y, dtype=float)
    horizontal = enc.get("horizontal", False)
    stacked = enc.get("stacked", False)

    unique_x = list(dict.fromkeys(x))
    n_colors = len(groups)
    x_pos = np.arange(len(unique_x))

    if stacked:
        bottom = np.zeros(len(unique_x))
        for cat, color, mask in groups:
            heights = np.array([float(np.sum(y[(x == x_val) & mask]))
                                for x_val in unique_x])
            bar_kwargs = dict(extra_kwargs, label=cat, color=color)
            if horizontal:
                axes.barh(x_pos, heights, left=bottom, **bar_kwargs)
            else:
                axes.bar(x_pos, heights, bottom=bottom, **bar_kwargs)
            bottom += heights
    else:
        width = 0.8 / n_colors
        for i, (cat, color, mask) in enumerate(groups):
            heights = np.array([float(np.sum(y[(x == x_val) & mask]))
                                for x_val in unique_x])
            offset = x_pos + (i - n_colors / 2 + 0.5) * width
            bar_kwargs = dict(extra_kwargs, label=cat, color=color)
            if horizontal:
                axes.barh(offset, heights, height=width, **bar_kwargs)
            else:
                axes.bar(offset, heights, width=width, **bar_kwargs)

    if horizontal:
        axes.set_yticks(x_pos, labels=unique_x)
    else:
        axes.set_xticks(x_pos, labels=unique_x)


def _render_wide_form(layer, adapter, axes, enc):
    """Render grouped bars — one cluster per x value, one bar per y-column."""
    x_raw = adapter.resolve(layer.x)
    series = adapter.resolve(layer.y)
    n_series = len(series)

    if series and len(series[0]) != len(x_raw):
        check_array_lengths({"x": x_raw, layer.y[0]: series[0]}, "bar")

    kwargs = dict(layer.kwargs)
    colors = default_colors(n_series, palette=layer.palette)
    x_pos = np.arange(len(x_raw))
    width = 0.8 / n_series

    horizontal = enc.get("horizontal", False)

    for i, (name, y_data) in enumerate(zip(layer.y, series)):
        offset = x_pos + (i - n_series / 2 + 0.5) * width
        series_kwargs = dict(kwargs, label=name, color=colors[i])
        if horizontal:
            axes.barh(offset, y_data, height=width, **series_kwargs)
        else:
            axes.bar(offset, y_data, width=width, **series_kwargs)

    if horizontal:
        axes.set_yticks(x_pos, labels=x_raw)
    else:
        axes.set_xticks(x_pos, labels=x_raw)
