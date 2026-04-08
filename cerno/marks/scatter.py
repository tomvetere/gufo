"""Scatter mark."""
import numpy as np

from ..core.validate import check_array_lengths, warn_nan_inf
from ._base import (
    apply_label, is_wide_form, render_wide_form, resolve_color, iter_color_groups,
)


def _draw_scatter(axes, x, y_data, **kwargs):
    axes.scatter(x, y_data, **kwargs)


def render(layer, adapter, axes):
    enc = layer.encodings

    if is_wide_form(layer.y):
        extra = {}
        if enc.get("alpha") is not None:
            extra["alpha"] = enc["alpha"]
        render_wide_form(layer, adapter, axes, _draw_scatter, **extra)
        return

    x = adapter.resolve(layer.x)
    y = adapter.resolve(layer.y)
    kwargs = dict(layer.kwargs)

    check_array_lengths({"x": x, "y": y}, "scatter")
    warn_nan_inf(x, "x", "scatter")
    warn_nan_inf(y, "y", "scatter")

    if enc.get("alpha") is not None:
        kwargs["alpha"] = enc["alpha"]
    apply_label(kwargs, enc)

    size_enc = enc.get("size")
    color_value = resolve_color(adapter, enc.get("color"))

    groups = iter_color_groups(color_value)
    if groups is not None:
        sz = adapter.resolve(size_enc) if size_enc is not None else None
        for cat, color, mask in groups:
            scatter_kwargs = dict(kwargs, label=cat)
            if sz is not None:
                scatter_kwargs["s"] = _normalize_size(sz[mask])
            axes.scatter(x[mask], y[mask], color=color, **scatter_kwargs)
        return

    if color_value is not None:
        if hasattr(color_value, "__len__") and len(color_value) == len(x):
            kwargs["c"] = color_value
        else:
            kwargs["color"] = color_value

    if size_enc is not None:
        sz = adapter.resolve(size_enc)
        kwargs["s"] = _normalize_size(sz)

    axes.scatter(x, y, **kwargs)


def _normalize_size(arr, min_size=20, max_size=400):
    arr = np.asarray(arr, dtype=float)
    if len(arr) == 0:
        return np.array([], dtype=float)
    lo, hi = arr.min(), arr.max()
    if hi == lo:
        return np.full(len(arr), (min_size + max_size) / 2)
    return min_size + (arr - lo) / (hi - lo) * (max_size - min_size)
