"""Histogram mark."""
from dataclasses import replace

import numpy as np

from ..core.validate import check_numeric, warn_nan_inf
from ._base import apply_color, apply_label, iter_color_groups, resolve_color

_VALID_MULTIPLE = ("layer", "stack", "dodge")


def render(layer, adapter, axes):
    x = adapter.resolve(layer.x)
    enc = layer.encodings
    kwargs = dict(layer.kwargs)

    check_numeric(x, "x", "histogram")
    warn_nan_inf(x, "x", "histogram")

    bins = enc.get("bins", "auto")
    density = enc.get("density", False)
    horizontal = enc.get("horizontal", False)
    multiple = enc.get("multiple", "layer")
    fill = enc.get("fill", True)

    if multiple not in _VALID_MULTIPLE:
        raise ValueError(
            f"histogram multiple must be one of {_VALID_MULTIPLE}, "
            f"got {multiple!r}"
        )

    kde_config = enc.get("kde")
    if kde_config is not None and multiple != "layer":
        raise ValueError(
            f"kde overlay requires multiple='layer', got {multiple!r}"
        )

    color_value = resolve_color(adapter, enc.get("color"))
    groups = iter_color_groups(color_value, palette=layer.palette,
                               color_order=enc.get("color_order"))

    curves = []  # (values, group, group color, counts, edges) for kde=
    if groups is not None:
        if multiple == "layer":
            curves = _render_layer(x, groups, axes, bins, density, horizontal,
                                   fill, kwargs)
        elif multiple == "stack":
            _render_stack(x, groups, axes, bins, density, horizontal, fill,
                          kwargs)
        else:
            _render_dodge(x, groups, axes, bins, density, horizontal, fill,
                          kwargs)
    else:
        kwargs["bins"] = bins
        kwargs["density"] = density
        if horizontal:
            kwargs["orientation"] = "horizontal"
        if not fill:
            kwargs["histtype"] = "step"
        apply_label(kwargs, enc)
        apply_color(kwargs, adapter, enc)
        counts, edges, _ = axes.hist(x, **kwargs)
        curves = [(x, None, None, counts, edges)]

    if kde_config is None:
        return
    for values, cat, color, counts, edges in curves:
        config = kde_config
        if cat is not None:
            # The bars already give each group a legend entry, so a curve
            # gets one only when the user named it.
            label = (f"{kde_config.label} ({cat})" if kde_config.label
                     else "_nolegend_")
            config = replace(kde_config, color=kde_config.color or color,
                             label=label)
        config._render(values, axes, scale=_kde_scale(values, counts, edges),
                       horizontal=horizontal)


def _kde_scale(values, counts, edges):
    """Factor that draws a density curve (area 1) in the bars' units.

    The bars' area covers only the values inside the bins, but the curve is
    fitted to all of them, so the area is spread over n_fitted / n_inside.
    """
    values = np.asarray(values, dtype=float)
    finite = values[np.isfinite(values)]
    inside = np.count_nonzero((finite >= edges[0]) & (finite <= edges[-1]))
    if inside == 0:
        return 0.0
    area = np.sum(counts * np.diff(edges))
    return float(area * len(finite) / inside)


def _render_layer(x, groups, axes, bins, density, horizontal, fill, kwargs):
    """Overlay histograms with transparency.

    Returns (values, group, color, counts, edges) per group for kde=.
    """
    hist_kwargs = dict(kwargs, bins=bins, density=density)
    if horizontal:
        hist_kwargs["orientation"] = "horizontal"
    if not fill:
        hist_kwargs["histtype"] = "step"

    alpha = hist_kwargs.pop("alpha", 0.6)
    curves = []
    for cat, color, mask in groups:
        counts, edges, _ = axes.hist(x[mask], color=color, label=cat,
                                     alpha=alpha, **hist_kwargs)
        curves.append((x[mask], cat, color, counts, edges))
    return curves


def _apply_fill_style(bar_kwargs, color, fill):
    """Set bar color or outline-only style based on fill flag."""
    if fill:
        bar_kwargs["color"] = color
    else:
        bar_kwargs["facecolor"] = "none"
        bar_kwargs["edgecolor"] = color


def _render_stack(x, groups, axes, bins, density, horizontal, fill, kwargs):
    """Stack histograms using bar() with cumulative bottom."""
    edges = np.histogram_bin_edges(x, bins=bins)
    width = np.diff(edges)
    centers = edges[:-1] + width / 2

    bottom = np.zeros(len(centers))
    for cat, color, mask in groups:
        counts, _ = np.histogram(x[mask], bins=edges, density=density)
        bar_kwargs = dict(kwargs, label=cat)
        _apply_fill_style(bar_kwargs, color, fill)

        if horizontal:
            axes.barh(centers, counts, height=width, left=bottom, **bar_kwargs)
        else:
            axes.bar(centers, counts, width=width, bottom=bottom, **bar_kwargs)
        bottom += counts


def _render_dodge(x, groups, axes, bins, density, horizontal, fill, kwargs):
    """Dodge histograms side-by-side using bar() with offsets."""
    edges = np.histogram_bin_edges(x, bins=bins)
    full_width = np.diff(edges)
    n = len(groups)
    sub_width = full_width / n
    centers = edges[:-1] + full_width / 2

    for i, (cat, color, mask) in enumerate(groups):
        counts, _ = np.histogram(x[mask], bins=edges, density=density)
        offset = centers + (i - n / 2 + 0.5) * sub_width
        bar_kwargs = dict(kwargs, label=cat)
        _apply_fill_style(bar_kwargs, color, fill)

        if horizontal:
            axes.barh(offset, counts, height=sub_width, **bar_kwargs)
        else:
            axes.bar(offset, counts, width=sub_width, **bar_kwargs)
