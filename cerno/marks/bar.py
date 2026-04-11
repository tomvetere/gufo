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


def _draw_dodged(axes, x_pos, series_list, horizontal, extra_kwargs):
    """Draw dodged (side-by-side) bars.

    series_list is [(heights, label, color), ...].
    """
    n = len(series_list)
    width = 0.8 / n
    for i, (heights, label, color) in enumerate(series_list):
        offset = x_pos + (i - n / 2 + 0.5) * width
        kw = dict(extra_kwargs, label=label, color=color)
        if horizontal:
            axes.barh(offset, heights, height=width, **kw)
        else:
            axes.bar(offset, heights, width=width, **kw)


def _set_category_ticks(axes, x_pos, labels, horizontal):
    """Set tick positions and labels for categorical bars."""
    if horizontal:
        axes.set_yticks(x_pos, labels=labels)
    else:
        axes.set_xticks(x_pos, labels=labels)


def _aggregate_by_x(x, y, mask, unique_x, x_indices):
    """Sum y values per unique x category, optionally filtered by mask."""
    if mask is not None:
        return np.bincount(x_indices[mask], weights=y[mask],
                           minlength=len(unique_x)).astype(float)
    return np.bincount(x_indices, weights=y,
                       minlength=len(unique_x)).astype(float)


def _render_color_groups(x, y, groups, axes, enc, extra_kwargs):
    """Render dodged or stacked bars grouped by a categorical color column."""
    x = np.asarray(x)
    y = np.asarray(y, dtype=float)
    horizontal = enc.get("horizontal", False)
    stacked = enc.get("stacked", False)

    unique_x = list(dict.fromkeys(x))
    x_pos = np.arange(len(unique_x))
    x_to_idx = {val: i for i, val in enumerate(unique_x)}
    x_indices = np.array([x_to_idx[v] for v in x])

    if stacked:
        bottom = np.zeros(len(unique_x))
        for cat, color, mask in groups:
            heights = _aggregate_by_x(x, y, mask, unique_x, x_indices)
            bar_kwargs = dict(extra_kwargs, label=cat, color=color)
            if horizontal:
                axes.barh(x_pos, heights, left=bottom, **bar_kwargs)
            else:
                axes.bar(x_pos, heights, bottom=bottom, **bar_kwargs)
            bottom += heights
    else:
        series = [(_aggregate_by_x(x, y, mask, unique_x, x_indices), cat, color)
                  for cat, color, mask in groups]
        _draw_dodged(axes, x_pos, series, horizontal, extra_kwargs)

    _set_category_ticks(axes, x_pos, unique_x, horizontal)


def _render_wide_form(layer, adapter, axes, enc):
    """Render grouped bars — one cluster per x value, one bar per y-column."""
    x_raw = adapter.resolve(layer.x)
    series = adapter.resolve(layer.y)
    n_series = len(series)

    if series and len(series[0]) != len(x_raw):
        check_array_lengths({"x": x_raw, layer.y[0]: series[0]}, "bar")

    colors = default_colors(n_series, palette=layer.palette)
    x_pos = np.arange(len(x_raw))
    horizontal = enc.get("horizontal", False)

    series_list = [(y_data, name, colors[i])
                   for i, (name, y_data) in enumerate(zip(layer.y, series))]
    _draw_dodged(axes, x_pos, series_list, horizontal, layer.kwargs)
    _set_category_ticks(axes, x_pos, x_raw, horizontal)
