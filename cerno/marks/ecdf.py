"""ECDF mark — empirical cumulative distribution function."""
import numpy as np

from ..core.validate import check_numeric, warn_nan_inf
from ._base import apply_color, apply_label, iter_color_groups, resolve_color


def render(layer, adapter, axes):
    enc = layer.encodings
    x = adapter.resolve(layer.x)
    kwargs = dict(layer.kwargs)

    check_numeric(x, "x", "ecdf")
    warn_nan_inf(x, "x", "ecdf")

    color_value = resolve_color(adapter, enc.get("color"))
    groups = iter_color_groups(color_value, palette=layer.palette)

    if groups is not None:
        for cat, color, mask in groups:
            _draw_ecdf(axes, x[mask], dict(kwargs, color=color, label=cat))
        return

    apply_label(kwargs, enc)
    apply_color(kwargs, adapter, enc)
    _draw_ecdf(axes, x, kwargs)


def _draw_ecdf(axes, x, kwargs):
    """Draw a single ECDF step function."""
    x = np.asarray(x, dtype=float)
    x = x[np.isfinite(x)]
    if len(x) == 0:
        return
    sorted_x = np.sort(x)
    n = len(sorted_x)
    y = np.arange(1, n + 1) / n
    axes.step(sorted_x, y, where="post", **kwargs)
