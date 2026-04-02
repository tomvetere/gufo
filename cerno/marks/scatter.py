"""Scatter mark."""
from ..data.inference import is_categorical
from ._base import resolve_color, default_colors


def render(layer, adapter, axes):
    x = adapter.resolve(layer.x)
    y = adapter.resolve(layer.y)
    enc = layer.encodings
    kwargs = dict(layer.kwargs)

    if enc.get("alpha") is not None:
        kwargs["alpha"] = enc["alpha"]
    if enc.get("label") is not None:
        kwargs["label"] = enc["label"]

    size_enc = enc.get("size")
    color_value = resolve_color(adapter, enc.get("color"))

    # Categorical color → one scatter call per category
    if color_value is not None and hasattr(color_value, "__len__") and is_categorical(color_value):
        categories = list(dict.fromkeys(color_value))
        cmap = default_colors(len(categories))
        color_map = {cat: cmap[i] for i, cat in enumerate(categories)}
        for cat in categories:
            mask = color_value == cat
            scatter_kwargs = dict(kwargs, label=cat)
            if size_enc is not None:
                sz = adapter.resolve(size_enc)
                scatter_kwargs["s"] = _normalize_size(sz[mask])
            axes.scatter(x[mask], y[mask], color=color_map[cat], **scatter_kwargs)
        return

    if color_value is not None:
        if hasattr(color_value, "__len__") and len(color_value) == len(x):
            kwargs["c"] = color_value
        else:
            kwargs["color"] = color_value

    if size_enc is not None:
        try:
            sz = adapter.resolve(size_enc)
            kwargs["s"] = _normalize_size(sz)
        except (KeyError, TypeError):
            pass

    axes.scatter(x, y, **kwargs)


def _normalize_size(arr, min_size=20, max_size=400):
    import numpy as np
    arr = arr.astype(float)
    if len(arr) == 0:
        return []
    lo, hi = arr.min(), arr.max()
    if hi == lo:
        return [100] * len(arr)
    return min_size + (arr - lo) / (hi - lo) * (max_size - min_size)
