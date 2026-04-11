"""Bar mark."""
import numpy as np

from ..core.validate import check_array_lengths, warn_nan_inf
from ._base import apply_label, apply_color, default_colors, is_wide_form, resolve_errors


def render(layer, adapter, axes):
    enc = layer.encodings

    if is_wide_form(layer.y):
        _render_wide_form(layer, adapter, axes, enc)
        return

    x = adapter.resolve(layer.x)
    y = adapter.resolve(layer.y)
    kwargs = dict(layer.kwargs)

    check_array_lengths({"x": x, "y": y}, "bar")
    warn_nan_inf(y, "y", "bar")

    apply_label(kwargs, enc)
    apply_color(kwargs, adapter, enc)

    yerr, xerr = resolve_errors(adapter, enc)
    if yerr is not None:
        kwargs["yerr"] = yerr
    if xerr is not None:
        kwargs["xerr"] = xerr

    if enc.get("horizontal"):
        axes.barh(x, y, **kwargs)
    else:
        axes.bar(x, y, **kwargs)


def _render_wide_form(layer, adapter, axes, enc):
    """Render grouped bars — one cluster per x value, one bar per y-column."""
    x_raw = adapter.resolve(layer.x)
    series = adapter.resolve(layer.y)
    n_series = len(series)

    if series and len(series[0]) != len(x_raw):
        check_array_lengths({"x": x_raw, layer.y[0]: series[0]}, "bar")

    kwargs = dict(layer.kwargs)
    colors = default_colors(n_series, palette=layer.palette)
    x_pos = np.arange(len(x_raw))
    width = 0.8 / n_series

    horizontal = enc.get("horizontal", False)

    for i, (name, y_data) in enumerate(zip(layer.y, series)):
        offset = x_pos + (i - n_series / 2 + 0.5) * width
        series_kwargs = dict(kwargs, label=name, color=colors[i])
        if horizontal:
            axes.barh(offset, y_data, height=width, **series_kwargs)
        else:
            axes.bar(offset, y_data, width=width, **series_kwargs)

    if horizontal:
        axes.set_yticks(x_pos, labels=x_raw)
    else:
        axes.set_xticks(x_pos, labels=x_raw)
