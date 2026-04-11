"""Rug mark — tick marks along an axis showing individual data points."""
from ._base import apply_label, iter_color_groups, resolve_color


def render(layer, adapter, axes):
    enc = layer.encodings
    x = adapter.resolve(layer.x)
    kwargs = dict(layer.kwargs)

    height = enc.get("height", 0.05)
    alpha = enc.get("alpha", 0.5)

    color_value = resolve_color(adapter, enc.get("color"))
    groups = iter_color_groups(color_value, palette=layer.palette)

    if groups is not None:
        for cat, color, mask in groups:
            axes.vlines(x[mask], 0, height,
                        transform=axes.get_xaxis_transform(),
                        color=color, alpha=alpha, label=cat, **kwargs)
        return

    apply_label(kwargs, enc)
    if color_value is not None and isinstance(color_value, str):
        kwargs["color"] = color_value

    axes.vlines(x, 0, height, transform=axes.get_xaxis_transform(),
                alpha=alpha, **kwargs)
