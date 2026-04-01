"""Line mark — supports single series, multi-series (wide-form), and color grouping."""
from ..data.inference import is_categorical

_DASH_STYLES = {
    "solid": "-",
    "dashed": "--",
    "dotted": ":",
    "dashdot": "-.",
}


def render(layer, adapter, axes):
    x = adapter.resolve(layer.x)
    enc = layer.encodings
    kwargs = dict(layer.kwargs)

    linestyle = _DASH_STYLES.get(enc.get("stroke_dash", "solid"), "-")
    kwargs["linestyle"] = linestyle

    if enc.get("label") is not None:
        kwargs["label"] = enc["label"]

    color_enc = enc.get("color")

    # Wide-form: y is a list of column names
    if isinstance(layer.y, list) and all(isinstance(k, str) for k in layer.y):
        series = adapter.resolve(layer.y)   # list of arrays
        colors = _default_colors(len(series))
        for i, (name, y_data) in enumerate(zip(layer.y, series)):
            series_kwargs = dict(kwargs, label=name, color=colors[i])
            axes.plot(x, y_data, **series_kwargs)
        return

    y = adapter.resolve(layer.y)

    # Long-form with color grouping
    if color_enc is not None and isinstance(color_enc, str):
        try:
            color_data = adapter.resolve(color_enc)
            if is_categorical(color_data):
                categories = list(dict.fromkeys(color_data))
                colors = _default_colors(len(categories))
                for i, cat in enumerate(categories):
                    mask = color_data == cat
                    series_kwargs = dict(kwargs, label=cat, color=colors[i])
                    axes.plot(x[mask], y[mask], **series_kwargs)
                return
        except (KeyError, TypeError):
            kwargs["color"] = color_enc

    if color_enc is not None and not isinstance(color_enc, str):
        kwargs["color"] = color_enc

    axes.plot(x, y, **kwargs)


def _default_colors(n):
    import matplotlib.pyplot as plt
    cmap = plt.get_cmap("tab10")
    return [cmap(i % 10) for i in range(n)]
