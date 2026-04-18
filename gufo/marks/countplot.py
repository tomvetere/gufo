"""Countplot mark — bar chart of value counts."""
import numpy as np

from ._base import (
    _resolve_order, apply_label, default_colors, iter_color_groups,
    resolve_color, resolve_color_list,
)


def render(layer, adapter, axes):
    enc = layer.encodings
    x = adapter.resolve(layer.x)
    kwargs = dict(layer.kwargs)
    horizontal = enc.get("horizontal", False)

    color_value = resolve_color(adapter, enc.get("color"))
    groups = iter_color_groups(color_value, palette=layer.palette,
                               color_order=enc.get("color_order"))

    if groups is not None:
        _render_grouped(x, color_value, groups, axes, enc, kwargs)
        return

    unique_x = _resolve_order(x, enc.get("order"))
    counts = [int(np.sum(x == val)) for val in unique_x]

    colors = resolve_color_list(adapter, enc, len(unique_x),
                                palette=layer.palette)
    apply_label(kwargs, enc)

    if horizontal:
        axes.barh(unique_x, counts, color=colors, **kwargs)
    else:
        axes.bar(unique_x, counts, color=colors, **kwargs)


def _render_grouped(x, color_value, groups, axes, enc, extra_kwargs):
    """Render grouped countplot — side-by-side bars per color category."""
    x = np.asarray(x)
    color_value = np.asarray(color_value)
    horizontal = enc.get("horizontal", False)

    unique_x = _resolve_order(x, enc.get("order"))
    n_colors = len(groups)
    x_pos = np.arange(len(unique_x))
    width = 0.8 / n_colors

    for i, (cat, color, _) in enumerate(groups):
        counts = [int(np.sum((x == x_val) & (color_value == cat)))
                  for x_val in unique_x]
        offset = x_pos + (i - n_colors / 2 + 0.5) * width
        kwargs = dict(extra_kwargs, label=cat, color=color)
        if horizontal:
            axes.barh(offset, counts, height=width, **kwargs)
        else:
            axes.bar(offset, counts, width=width, **kwargs)

    if horizontal:
        axes.set_yticks(x_pos, labels=unique_x)
    else:
        axes.set_xticks(x_pos, labels=unique_x)
