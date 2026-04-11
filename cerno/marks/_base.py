"""Shared utilities for mark renderers."""
import numpy as np

from ..core.validate import check_array_lengths, warn_nan_inf
from ..data.inference import is_categorical
from ..style.color import CERNO_PALETTE


def resolve_color(adapter, color_enc):
    """Resolve a color encoding: try as column name, fall back to literal.

    Returns resolved column data (numpy array) or the literal color value.
    Returns None if color_enc is None.
    """
    if color_enc is None:
        return None
    if not isinstance(color_enc, str):
        return color_enc
    try:
        return adapter.resolve(color_enc)
    except (KeyError, TypeError, ValueError):
        return color_enc


def default_colors(n, palette=None):
    """Return n colors from the palette, cycling if needed."""
    colors = palette if palette is not None else CERNO_PALETTE.categorical
    k = len(colors)
    return [colors[i % k] for i in range(n)]


def apply_label(kwargs, enc):
    """Copy the label encoding into kwargs if present."""
    if enc.get("label") is not None:
        kwargs["label"] = enc["label"]


def apply_color(kwargs, adapter, enc):
    """Resolve and apply a non-categorical color encoding to kwargs."""
    color_value = resolve_color(adapter, enc.get("color"))
    if color_value is not None:
        kwargs["color"] = color_value


def is_wide_form(layer_y):
    """Return True if y is a list of column name strings (wide-form)."""
    return isinstance(layer_y, list) and all(isinstance(k, str) for k in layer_y)


def render_wide_form(layer, adapter, axes, draw_fn, **extra_kwargs):
    """Render wide-form data by calling draw_fn once per y-column.

    draw_fn is called as draw_fn(axes, x, y_data, **kwargs) for each series.
    Only call this after checking is_wide_form(layer.y).
    """
    x = adapter.resolve(layer.x)
    series = adapter.resolve(layer.y)
    if series and len(series[0]) != len(x):
        check_array_lengths({"x": x, layer.y[0]: series[0]}, layer.mark_type)

    kwargs = dict(layer.kwargs, **extra_kwargs)
    colors = default_colors(len(series), palette=layer.palette)

    for i, (name, y_data) in enumerate(zip(layer.y, series)):
        series_kwargs = dict(kwargs, label=name, color=colors[i])
        draw_fn(axes, x, y_data, **series_kwargs)


def group_by_x(x, y):
    """Group y-values by unique x-values for distribution marks.

    Returns (unique_x, grouped, positions) where grouped is a list of
    y sub-arrays and positions is 1-based integers for matplotlib.
    """
    unique_x = list(dict.fromkeys(x))
    grouped = [y[x == val] for val in unique_x]
    positions = list(range(1, len(unique_x) + 1))
    return unique_x, grouped, positions


def iter_color_groups(color_value, palette=None):
    """Yield (category, color, mask) for each group in a categorical color array.

    Returns None if color_value is not categorical, allowing callers to
    fall through to the non-grouped code path.
    """
    if (color_value is None
            or isinstance(color_value, str)
            or not hasattr(color_value, "__len__")
            or not is_categorical(color_value)):
        return None
    categories = list(dict.fromkeys(color_value))
    colors = default_colors(len(categories), palette=palette)
    return [(cat, colors[i], color_value == cat) for i, cat in enumerate(categories)]


def resolve_color_list(adapter, enc, n, palette=None):
    """Resolve a color encoding to a list of n colors.

    If enc["color"] is a literal color string, repeat it n times.
    Otherwise return n default palette colors.
    """
    color = resolve_color(adapter, enc.get("color"))
    if color is not None and isinstance(color, str):
        return [color] * n
    return default_colors(n, palette=palette)


def resolve_errors(adapter, enc):
    """Resolve y_error / x_error encodings to arrays or None."""
    yerr = enc.get("y_error")
    xerr = enc.get("x_error")
    if yerr is not None:
        yerr = adapter.resolve(yerr) if isinstance(yerr, str) else np.asarray(yerr)
    if xerr is not None:
        xerr = adapter.resolve(xerr) if isinstance(xerr, str) else np.asarray(xerr)
    return yerr, xerr


def render_categorical_scatter(layer, adapter, axes, offset_fn, mark_name,
                               default_alpha=0.6, default_size=20):
    """Shared renderer for strip and swarm plots.

    offset_fn(values, enc) -> array of categorical-axis offsets per group.
    """
    enc = layer.encodings

    if is_wide_form(layer.y):
        _render_categorical_wide(layer, adapter, axes, enc, offset_fn,
                                 default_alpha, default_size)
        return

    x = adapter.resolve(layer.x)
    y = adapter.resolve(layer.y)
    kwargs = dict(layer.kwargs)

    check_array_lengths({"x": x, "y": y}, mark_name)
    warn_nan_inf(y, "y", mark_name)

    unique_x, grouped, positions = group_by_x(x, y)

    size = enc.get("size", default_size)
    alpha = enc.get("alpha", default_alpha)
    horizontal = enc.get("horizontal", False)
    colors = resolve_color_list(adapter, enc, len(unique_x),
                                palette=layer.palette)

    apply_label(kwargs, enc)

    for i, (pos, vals) in enumerate(zip(positions, grouped)):
        offsets = offset_fn(vals, enc)
        if horizontal:
            axes.scatter(vals, pos + offsets, s=size, alpha=alpha,
                         color=colors[i], **kwargs)
        else:
            axes.scatter(pos + offsets, vals, s=size, alpha=alpha,
                         color=colors[i], **kwargs)

    if horizontal:
        axes.set_yticks(positions, labels=unique_x)
    else:
        axes.set_xticks(positions, labels=unique_x)


def _render_categorical_wide(layer, adapter, axes, enc, offset_fn,
                              default_alpha, default_size):
    """Wide-form path for render_categorical_scatter."""
    series = adapter.resolve(layer.y)
    positions = list(range(1, len(layer.y) + 1))
    kwargs = dict(layer.kwargs)

    size = enc.get("size", default_size)
    alpha = enc.get("alpha", default_alpha)
    horizontal = enc.get("horizontal", False)
    colors = default_colors(len(layer.y), palette=layer.palette)

    apply_label(kwargs, enc)

    for i, (pos, vals) in enumerate(zip(positions, series)):
        offsets = offset_fn(vals, enc)
        if horizontal:
            axes.scatter(vals, pos + offsets, s=size, alpha=alpha,
                         color=colors[i], **kwargs)
        else:
            axes.scatter(pos + offsets, vals, s=size, alpha=alpha,
                         color=colors[i], **kwargs)

    set_category_ticks(axes, positions, layer.y, horizontal)


def set_category_ticks(axes, positions, labels, horizontal):
    """Set tick positions and labels, respecting orientation."""
    if horizontal:
        axes.set_yticks(positions, labels=labels)
    else:
        axes.set_xticks(positions, labels=labels)
