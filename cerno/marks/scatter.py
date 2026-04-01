"""Scatter mark."""
from ..data.inference import is_categorical


def render(layer, adapter, axes):
    x = adapter.resolve(layer.x)
    y = adapter.resolve(layer.y)
    enc = layer.encodings
    kwargs = dict(layer.kwargs)

    if enc.get("alpha") is not None:
        kwargs["alpha"] = enc["alpha"]
    if enc.get("label") is not None:
        kwargs["label"] = enc["label"]

    color_enc = enc.get("color")
    size_enc = enc.get("size")

    if color_enc is not None and isinstance(color_enc, str):
        try:
            color_data = adapter.resolve(color_enc)
            if is_categorical(color_data):
                categories = list(dict.fromkeys(color_data))
                cmap = _categorical_colors(len(categories))
                color_map = {cat: cmap[i] for i, cat in enumerate(categories)}
                for cat in categories:
                    mask = color_data == cat
                    scatter_kwargs = dict(kwargs, label=cat)
                    if size_enc is not None:
                        sz = adapter.resolve(size_enc)
                        scatter_kwargs["s"] = _normalize_size(sz[mask])
                    axes.scatter(x[mask], y[mask], color=color_map[cat], **scatter_kwargs)
                return
            else:
                kwargs["c"] = color_data
        except (KeyError, TypeError):
            kwargs["color"] = color_enc

    if size_enc is not None:
        try:
            sz = adapter.resolve(size_enc)
            kwargs["s"] = _normalize_size(sz)
        except (KeyError, TypeError):
            pass

    axes.scatter(x, y, **kwargs)


def _categorical_colors(n):
    import matplotlib.pyplot as plt
    cmap = plt.get_cmap("tab10")
    return [cmap(i % 10) for i in range(n)]


def _normalize_size(arr, min_size=20, max_size=400):
    import numpy as np
    arr = arr.astype(float)
    lo, hi = arr.min(), arr.max()
    if hi == lo:
        return [100] * len(arr)
    return min_size + (arr - lo) / (hi - lo) * (max_size - min_size)
