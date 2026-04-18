"""Line mark — supports single series, multi-series (wide-form), and color grouping."""
import numpy as np
from matplotlib.collections import LineCollection
from matplotlib.colors import Normalize

from ..core.validate import check_array_lengths, check_stroke_dash, warn_nan_inf
from ._base import (
    apply_label, is_continuous_color, is_wide_form, iter_color_groups,
    render_wide_form, resolve_color, resolve_color_range, resolve_errors,
)

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

    if is_wide_form(layer.y):
        render_wide_form(
            layer, adapter, axes,
            lambda axes, x, y_data, **kw: axes.plot(x, y_data, **kw),
            linestyle=linestyle,
        )
        return

    apply_label(kwargs, enc)

    color_enc = enc.get("color")

    y = adapter.resolve(layer.y)
    check_array_lengths({"x": x, "y": y}, "line")
    warn_nan_inf(x, "x", "line")
    warn_nan_inf(y, "y", "line")

    yerr, xerr = resolve_errors(adapter, enc)
    if yerr is not None or xerr is not None:
        color_value = resolve_color(adapter, color_enc)
        if color_value is not None and isinstance(color_value, str):
            kwargs["color"] = color_value
        kwargs.pop("linestyle", None)
        kwargs.setdefault("fmt", "-")
        axes.errorbar(x, y, yerr=yerr, xerr=xerr, **kwargs)
        return

    color_value = resolve_color(adapter, color_enc)
    groups = iter_color_groups(color_value, palette=layer.palette,
                               color_order=enc.get("color_order"))
    if groups is not None:
        for cat, color, mask in groups:
            series_kwargs = dict(kwargs, label=cat, color=color)
            axes.plot(x[mask], y[mask], **series_kwargs)
        return

    if is_continuous_color(color_value, len(x)):
        _draw_continuous_line(axes, x, y, color_value, enc, kwargs)
        return

    if color_value is not None:
        kwargs["color"] = color_value

    axes.plot(x, y, **kwargs)


def _draw_continuous_line(axes, x, y, color_value, enc, kwargs):
    """Draw a line whose segments are colored by a numeric variable."""
    arr = np.asarray(color_value, dtype=float)
    vmin, vmax = resolve_color_range(arr, enc.get("vmin"), enc.get("vmax"))

    points = np.array([x, y]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)
    segment_values = (arr[:-1] + arr[1:]) / 2

    lc_kwargs = {"cmap": enc.get("cmap"), "norm": Normalize(vmin=vmin, vmax=vmax)}
    if kwargs.get("linestyle") is not None:
        lc_kwargs["linestyles"] = kwargs["linestyle"]
    if kwargs.get("linewidth") is not None:
        lc_kwargs["linewidths"] = kwargs["linewidth"]
    if kwargs.get("label") is not None:
        lc_kwargs["label"] = kwargs["label"]

    lc = LineCollection(segments, **lc_kwargs)
    lc.set_array(segment_values)
    axes.add_collection(lc)
    axes.autoscale_view()

    if enc.get("colorbar", True):
        axes.figure.colorbar(lc, ax=axes)
