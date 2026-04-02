"""Bar mark."""
from ._base import resolve_color


def render(layer, adapter, axes):
    x = adapter.resolve(layer.x)
    y = adapter.resolve(layer.y)
    enc = layer.encodings
    kwargs = dict(layer.kwargs)

    if enc.get("label") is not None:
        kwargs["label"] = enc["label"]

    color_value = resolve_color(adapter, enc.get("color"))
    if color_value is not None:
        kwargs["color"] = color_value

    if enc.get("horizontal"):
        axes.barh(x, y, **kwargs)
    else:
        axes.bar(x, y, **kwargs)
