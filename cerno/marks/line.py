"""Line mark — supports single series, multi-series (wide-form), and color grouping."""
from ..data.inference import is_categorical
from ._base import resolve_color, default_colors

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
        colors = default_colors(len(series))
        for i, (name, y_data) in enumerate(zip(layer.y, series)):
            series_kwargs = dict(kwargs, label=name, color=colors[i])
            axes.plot(x, y_data, **series_kwargs)
        return

    y = adapter.resolve(layer.y)

    # Long-form with color grouping
    color_value = resolve_color(adapter, color_enc)
    if color_value is not None and hasattr(color_value, "__len__") and is_categorical(color_value):
        categories = list(dict.fromkeys(color_value))
        colors = default_colors(len(categories))
        for i, cat in enumerate(categories):
            mask = color_value == cat
            series_kwargs = dict(kwargs, label=cat, color=colors[i])
            axes.plot(x[mask], y[mask], **series_kwargs)
        return

    if color_value is not None:
        kwargs["color"] = color_value

    axes.plot(x, y, **kwargs)
