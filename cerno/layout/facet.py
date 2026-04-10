"""Facet rendering — split data by categorical columns into subplots."""
import math

import matplotlib.pyplot as plt
import numpy as np

from ..data.adapter import DataAdapter
from ..data.inference import is_categorical
from ..style.theme import _resolve_theme


def render_facet(chart, facet_column, wrap_cols=3, *, facet_row=None):
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

    Returns
    -------
    (fig, axes_2d) : tuple
        The matplotlib Figure and 2D array of Axes.
    """
    adapter = DataAdapter.from_any(chart._data)

    if facet_row is not None:
        return _render_two_variable(chart, adapter, facet_column, facet_row)
    return _render_one_variable(chart, adapter, facet_column, wrap_cols)


def _render_one_variable(chart, adapter, facet_column, wrap_cols):
    """Single-variable faceting — wrap panels into rows."""
    col_data = adapter.resolve(facet_column)
    _check_categorical(col_data, facet_column)

    categories = list(dict.fromkeys(col_data))
    n = len(categories)
    cols = min(n, wrap_cols)
    rows = math.ceil(n / cols)

    theme = _resolve_theme(chart._theme_override)

    with theme.as_context():
        fig, axes_grid = plt.subplots(rows, cols, figsize=_facet_figsize(rows, cols))
        axes_grid = np.atleast_2d(axes_grid).reshape(rows, cols)

        for i, category in enumerate(categories):
            r, c = divmod(i, cols)
            mask = col_data == category
            sub_adapter = adapter.subset(mask)
            chart._render_onto(fig, axes_grid[r, c], adapter=sub_adapter)
            axes_grid[r, c].set_title(str(category))

        for i in range(n, rows * cols):
            r, c = divmod(i, cols)
            axes_grid[r, c].set_visible(False)

        if chart._title:
            fig.suptitle(chart._title)

        fig.tight_layout()

    return fig, axes_grid


def _render_two_variable(chart, adapter, facet_column, facet_row):
    """Two-variable faceting — row categories × column categories."""
    row_data = adapter.resolve(facet_row)
    _check_categorical(row_data, facet_row)
    row_cats = list(dict.fromkeys(row_data))

    if facet_column is not None:
        col_data = adapter.resolve(facet_column)
        _check_categorical(col_data, facet_column)
        col_cats = list(dict.fromkeys(col_data))
    else:
        col_data = None
        col_cats = [None]

    n_rows = len(row_cats)
    n_cols = len(col_cats)
    theme = _resolve_theme(chart._theme_override)

    with theme.as_context():
        fig, axes_grid = plt.subplots(
            n_rows, n_cols, figsize=_facet_figsize(n_rows, n_cols))
        axes_grid = np.atleast_2d(axes_grid).reshape(n_rows, n_cols)

        for ri, row_val in enumerate(row_cats):
            row_mask = row_data == row_val
            for ci, col_val in enumerate(col_cats):
                if col_data is not None:
                    mask = row_mask & (col_data == col_val)
                else:
                    mask = row_mask

                if mask.any():
                    sub_adapter = adapter.subset(mask)
                    chart._render_onto(fig, axes_grid[ri, ci], adapter=sub_adapter)
                else:
                    axes_grid[ri, ci].set_visible(False)

                if ri == 0 and col_val is not None:
                    axes_grid[ri, ci].set_title(str(col_val))

            axes_grid[ri, 0].set_ylabel(str(row_val))

        if chart._title:
            fig.suptitle(chart._title)

        fig.tight_layout()

    return fig, axes_grid


def _check_categorical(data, column_name):
    if not is_categorical(data):
        raise ValueError(
            f"facet(): column '{column_name}' is not categorical. "
            "Faceting requires a categorical column (strings or pandas Categorical)."
        )


def _facet_figsize(rows, cols, cell_width=4.5, cell_height=3.5):
    """Compute a reasonable figure size from the grid dimensions."""
    return (cols * cell_width, rows * cell_height)
