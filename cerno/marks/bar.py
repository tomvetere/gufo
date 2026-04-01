"""Bar mark."""


def render(layer, adapter, axes):
    x = adapter.resolve(layer.x)
    y = adapter.resolve(layer.y)
    enc = layer.encodings
    kwargs = dict(layer.kwargs)

    if enc.get("label") is not None:
        kwargs["label"] = enc["label"]

    color_enc = enc.get("color")
    if color_enc is not None:
        try:
            kwargs["color"] = adapter.resolve(color_enc)
        except (KeyError, TypeError):
            kwargs["color"] = color_enc

    if enc.get("horizontal"):
        axes.barh(x, y, **kwargs)
    else:
        axes.bar(x, y, **kwargs)
