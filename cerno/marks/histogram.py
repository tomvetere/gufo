"""Histogram mark."""


def render(layer, adapter, axes):
    x = adapter.resolve(layer.x)
    enc = layer.encodings
    kwargs = dict(layer.kwargs)

    kwargs["bins"] = enc.get("bins", "auto")

    if enc.get("label") is not None:
        kwargs["label"] = enc["label"]

    color_enc = enc.get("color")
    if color_enc is not None:
        try:
            kwargs["color"] = adapter.resolve(color_enc)
        except (KeyError, TypeError):
            kwargs["color"] = color_enc

    axes.hist(x, **kwargs)
