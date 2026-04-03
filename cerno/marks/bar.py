"""Bar mark."""
from ..core.validate import check_array_lengths, warn_nan_inf
from ._base import apply_label, apply_color


def render(layer, adapter, axes):
    x = adapter.resolve(layer.x)
    y = adapter.resolve(layer.y)
    enc = layer.encodings
    kwargs = dict(layer.kwargs)

    check_array_lengths({"x": x, "y": y}, "bar")
    warn_nan_inf(y, "y", "bar")

    apply_label(kwargs, enc)
    apply_color(kwargs, adapter, enc)

    if enc.get("horizontal"):
        axes.barh(x, y, **kwargs)
    else:
        axes.bar(x, y, **kwargs)
