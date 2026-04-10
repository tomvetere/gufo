"""Histogram mark."""
from ..core.validate import check_numeric, warn_nan_inf
from ._base import apply_color, apply_label, iter_color_groups, resolve_color


def render(layer, adapter, axes):
    x = adapter.resolve(layer.x)
    enc = layer.encodings
    kwargs = dict(layer.kwargs)

    check_numeric(x, "x", "histogram")
    warn_nan_inf(x, "x", "histogram")

    kwargs["bins"] = enc.get("bins", "auto")

    color_value = resolve_color(adapter, enc.get("color"))
    groups = iter_color_groups(color_value)

    if groups is not None:
        alpha = kwargs.pop("alpha", 0.6)
        for cat, color, mask in groups:
            axes.hist(x[mask], color=color, label=cat, alpha=alpha, **kwargs)
        return

    apply_label(kwargs, enc)
    apply_color(kwargs, adapter, enc)

    axes.hist(x, **kwargs)
