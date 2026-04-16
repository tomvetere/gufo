"""Facet rendering — split data by categorical columns into subplots."""
import math
import warnings
from contextlib import contextmanager
from dataclasses import replace

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.cm import ScalarMappable
from matplotlib.colors import Normalize

from ..data.adapter import DataAdapter
from ..data.inference import is_categorical
from ..marks._base import resolve_color_range
from ..style.theme import _resolve_theme

_CONTINUOUS_COLOR_MARKS = ("scatter", "line")


def render_facet(chart, facet_column, wrap_cols=3, *, facet_row=None,
                 sharex=True, sharey=True):
    """Render a Chart as a faceted grid of subplots.

    Parameters
    ----------
    chart : Chart
        The chart whose layers, decorators, and apply funcs to render.
    facet_column : str or None
        Column name for the column dimension. When used alone, panels
        wrap after wrap_cols columns.
    wrap_cols : int
        Maximum number of columns before wrapping (single-variable only).
    facet_row : str or None
        Column name for the row dimension. When combined with
        facet_column, creates a rows × cols grid.
    sharex : bool
        Share x-axis range across panels. Default True.
    sharey : bool
        Share y-axis range across panels. Default True.

    Returns
    -------
    (fig, axes_2d) : tuple
        The matplotlib Figure and 2D array of Axes.
    """
    adapter = DataAdapter.from_any(chart._data)

    if facet_row is not None:
        return _render_two_variable(chart, adapter, facet_column, facet_row,
                                    sharex=sharex, sharey=sharey)
    return _render_one_variable(chart, adapter, facet_column, wrap_cols,
                                sharex=sharex, sharey=sharey)


def _render_one_variable(chart, adapter, facet_column, wrap_cols, *,
                         sharex=True, sharey=True):
    """Single-variable faceting — wrap panels into rows."""
    col_data = adapter.resolve(facet_column)
    _check_categorical(col_data, facet_column)

    categories = _unique_categories(col_data, facet_column)
    n = len(categories)
    cols = min(n, wrap_cols)
    rows = math.ceil(n / cols)

    theme = _resolve_theme(chart._theme_override)

    with theme.as_context():
        fig, axes_grid = plt.subplots(rows, cols, figsize=_facet_figsize(rows, cols),
                                      sharex=sharex, sharey=sharey,
                                      layout="constrained")
        axes_grid = np.atleast_2d(axes_grid).reshape(rows, cols)

        with _patched_layers(chart, adapter) as shared_bars:
            for i, category in enumerate(categories):
                r, c = divmod(i, cols)
                mask = col_data == category
                sub_adapter = adapter.subset(mask)
                chart._render_onto(fig, axes_grid[r, c], adapter=sub_adapter,
                                   suppress_legend=True)
                axes_grid[r, c].set_title(str(category))

            for i in range(n, rows * cols):
                r, c = divmod(i, cols)
                axes_grid[r, c].set_visible(False)

            visible_axes = [axes_grid[divmod(i, cols)] for i in range(n)]
            _draw_shared_colorbars(fig, visible_axes, shared_bars)
            _draw_shared_legend(fig, visible_axes, chart)

        if chart._title:
            fig.suptitle(chart._title)

    return fig, axes_grid


def _render_two_variable(chart, adapter, facet_column, facet_row, *,
                         sharex=True, sharey=True):
    """Two-variable faceting — row categories × column categories."""
    row_data = adapter.resolve(facet_row)
    _check_categorical(row_data, facet_row)
    row_cats = _unique_categories(row_data, facet_row)

    if facet_column is not None:
        col_data = adapter.resolve(facet_column)
        _check_categorical(col_data, facet_column)
        col_cats = _unique_categories(col_data, facet_column)
    else:
        col_data = None
        col_cats = [None]

    n_rows = len(row_cats)
    n_cols = len(col_cats)
    theme = _resolve_theme(chart._theme_override)

    with theme.as_context():
        fig, axes_grid = plt.subplots(
            n_rows, n_cols, figsize=_facet_figsize(n_rows, n_cols),
            sharex=sharex, sharey=sharey, layout="constrained")
        axes_grid = np.atleast_2d(axes_grid).reshape(n_rows, n_cols)

        with _patched_layers(chart, adapter) as shared_bars:
            visible_axes = []
            for ri, row_val in enumerate(row_cats):
                row_mask = row_data == row_val
                for ci, col_val in enumerate(col_cats):
                    if col_data is not None:
                        mask = row_mask & (col_data == col_val)
                    else:
                        mask = row_mask

                    if mask.any():
                        sub_adapter = adapter.subset(mask)
                        chart._render_onto(fig, axes_grid[ri, ci],
                                           adapter=sub_adapter,
                                           suppress_legend=True)
                        visible_axes.append(axes_grid[ri, ci])
                    else:
                        axes_grid[ri, ci].set_visible(False)

                    if ri == 0 and col_val is not None:
                        axes_grid[ri, ci].set_title(str(col_val))

                axes_grid[ri, 0].set_ylabel(str(row_val))

            _draw_shared_colorbars(fig, visible_axes, shared_bars)
            _draw_shared_legend(fig, visible_axes, chart)

        if chart._title:
            fig.suptitle(chart._title)

    return fig, axes_grid


def _unique_categories(col_data, column_name):
    """Extract unique categories, filtering NaN and warning if any are found."""
    def _is_nan(v):
        try:
            return np.isnan(v)
        except (TypeError, ValueError):
            return False

    categories = list(dict.fromkeys(col_data))
    clean = [c for c in categories if not _is_nan(c)]
    if len(clean) < len(categories):
        n_nan = sum(1 for v in col_data if _is_nan(v))
        warnings.warn(
            f"facet(): column '{column_name}' contains {n_nan} NaN value(s). "
            f"These rows are excluded from the faceted plot.",
            stacklevel=4,
        )
    return clean


def _check_categorical(data, column_name):
    if not is_categorical(data):
        raise ValueError(
            f"facet(): column '{column_name}' is not categorical. "
            "Faceting requires a categorical column (strings or pandas Categorical)."
        )


@contextmanager
def _patched_layers(chart, adapter):
    """Temporarily replace chart layers with shared-color-scale copies."""
    patched, shared_bars = _shared_color_scales(chart, adapter)
    original = chart._layers
    chart._layers = patched
    try:
        yield shared_bars
    finally:
        chart._layers = original


def _facet_figsize(rows, cols, cell_width=4.5, cell_height=3.5):
    """Compute a reasonable figure size from the grid dimensions."""
    return (cols * cell_width, rows * cell_height)


def _shared_color_scales(chart, full_adapter):
    """Build patched layer copies so all facet panels share a global color scale.

    Returns (patched_layers, descriptors). patched_layers is a list matching
    chart._layers where continuous-color layers have vmin/vmax/colorbar
    overridden. The original chart._layers are never mutated.
    """
    patched_layers = []
    descriptors = []
    for layer in chart._layers:
        if layer.mark_type not in _CONTINUOUS_COLOR_MARKS:
            patched_layers.append(layer)
            continue
        enc = layer.encodings
        color_enc = enc.get("color")
        if not isinstance(color_enc, str):
            patched_layers.append(layer)
            continue
        try:
            values = full_adapter.resolve(color_enc)
        except (KeyError, TypeError, ValueError):
            patched_layers.append(layer)
            continue
        if is_categorical(values):
            patched_layers.append(layer)
            continue
        if enc.get("colorbar") is False:
            patched_layers.append(layer)
            continue

        arr = np.asarray(values, dtype=float)
        if not np.isfinite(arr).any():
            patched_layers.append(layer)
            continue

        vmin, vmax = resolve_color_range(arr, enc.get("vmin"), enc.get("vmax"))

        new_enc = {**enc, "vmin": vmin, "vmax": vmax, "colorbar": False}
        patched_layers.append(replace(layer, encodings=new_enc))

        descriptors.append({
            "cmap": enc.get("cmap"),
            "vmin": vmin,
            "vmax": vmax,
            "label": color_enc,
        })

    return patched_layers, descriptors


def _draw_shared_colorbars(fig, axes_list, descriptors):
    """Draw one figure-level colorbar per shared-scale descriptor."""
    if not descriptors or not axes_list:
        return
    for desc in descriptors:
        norm = Normalize(vmin=desc["vmin"], vmax=desc["vmax"])
        sm = ScalarMappable(norm=norm, cmap=desc["cmap"])
        sm.set_array([])
        cbar = fig.colorbar(sm, ax=axes_list, shrink=0.9)
        if desc.get("label"):
            cbar.set_label(desc["label"])


def _draw_shared_legend(fig, axes_list, chart):
    """Collect handles from every panel and draw a single figure-level legend.

    Dedupes by label so categories shared across panels appear once.
    """
    opts = chart._legend_opts
    if not opts or opts.get("hide") or not axes_list:
        return

    seen = {}
    for ax in axes_list:
        handles, labels = ax.get_legend_handles_labels()
        for handle, label in zip(handles, labels):
            if label and label not in seen:
                seen[label] = handle

    if not seen:
        return

    labels = list(seen.keys())
    handles = list(seen.values())
    title = opts.get("title")
    position = opts.get("position", "best")

    # Figure-level anchors use flush figure-edge coordinates (1.0, 0.0, etc.),
    # unlike Chart._OUTSIDE_LEGEND which overshoots axes boxes at (1.02, ...).
    outside = {
        "outside right": {"bbox_to_anchor": (1.0, 0.5), "loc": "center left"},
        "outside left": {"bbox_to_anchor": (0.0, 0.5), "loc": "center right"},
        "outside top": {"bbox_to_anchor": (0.5, 1.0), "loc": "lower center"},
        "outside bottom": {"bbox_to_anchor": (0.5, 0.0), "loc": "upper center"},
    }
    if position == "best":
        kw = outside["outside right"]
    else:
        kw = outside.get(position, {"loc": position})
    fig.legend(handles, labels, title=title, **kw)
