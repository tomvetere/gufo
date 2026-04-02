"""Histogram mark."""
from ._base import resolve_color


def render(layer, adapter, axes):
    x = adapter.resolve(layer.x)
    enc = layer.encodings
    kwargs = dict(layer.kwargs)

    kwargs["bins"] = enc.get("bins", "auto")

    if enc.get("label") is not None:
        kwargs["label"] = enc["label"]

    color_value = resolve_color(adapter, enc.get("color"))
    if color_value is not None:
        kwargs["color"] = color_value

    axes.hist(x, **kwargs)
