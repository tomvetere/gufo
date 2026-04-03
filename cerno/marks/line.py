"""Line mark — supports single series, multi-series (wide-form), and color grouping."""
from ..core.validate import check_array_lengths, check_stroke_dash, warn_nan_inf
from ._base import apply_label, resolve_color, default_colors, iter_color_groups

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

    check_stroke_dash(enc.get("stroke_dash"), _DASH_STYLES)
    linestyle = _DASH_STYLES.get(enc.get("stroke_dash", "solid"), "-")
    kwargs["linestyle"] = linestyle

    apply_label(kwargs, enc)

    color_enc = enc.get("color")

    # Wide-form: y is a list of column names
    if isinstance(layer.y, list) and all(isinstance(k, str) for k in layer.y):
        series = adapter.resolve(layer.y)   # list of arrays
        if series and len(series[0]) != len(x):
            check_array_lengths({"x": x, layer.y[0]: series[0]}, "line")
        colors = default_colors(len(series))
        for i, (name, y_data) in enumerate(zip(layer.y, series)):
            series_kwargs = dict(kwargs, label=name, color=colors[i])
            axes.plot(x, y_data, **series_kwargs)
        return

    y = adapter.resolve(layer.y)
    check_array_lengths({"x": x, "y": y}, "line")
    warn_nan_inf(x, "x", "line")
    warn_nan_inf(y, "y", "line")

    color_value = resolve_color(adapter, color_enc)
    groups = iter_color_groups(color_value)
    if groups is not None:
        for cat, color, mask in groups:
            series_kwargs = dict(kwargs, label=cat, color=color)
            axes.plot(x[mask], y[mask], **series_kwargs)
        return

    if color_value is not None:
        kwargs["color"] = color_value

    axes.plot(x, y, **kwargs)
