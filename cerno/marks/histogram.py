"""Histogram mark."""
from ..core.validate import check_numeric, warn_nan_inf
from ._base import apply_label, apply_color


def render(layer, adapter, axes):
    x = adapter.resolve(layer.x)
    enc = layer.encodings
    kwargs = dict(layer.kwargs)

    check_numeric(x, "x", "histogram")
    warn_nan_inf(x, "x", "histogram")

    kwargs["bins"] = enc.get("bins", "auto")

    apply_label(kwargs, enc)
    apply_color(kwargs, adapter, enc)

    axes.hist(x, **kwargs)
