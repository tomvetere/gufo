"""Facet rendering — split data by a categorical column into subplots."""
import math

import matplotlib.pyplot as plt
import numpy as np

from ..data.adapter import DataAdapter
from ..data.inference import is_categorical
from ..style.theme import _resolve_theme


def render_facet(chart, facet_column, wrap_cols=3):
    """Render a Chart as a faceted grid of subplots.

    Each unique value in facet_column gets its own subplot, showing the
    same layers with only that subset of data. Panels wrap into rows
    after wrap_cols columns.

    Parameters
    ----------
    chart : Chart
        The chart whose layers, decorators, and apply funcs to render.
    facet_column : str
        Column name to split on. Must be categorical.
    wrap_cols : int
        Maximum number of columns before wrapping to a new row.

    Returns
    -------
    (fig, axes_2d) : tuple
        The matplotlib Figure and 2D array of Axes.
    """
    adapter = DataAdapter.from_any(chart._data)
    col_data = adapter.resolve(facet_column)

    if not is_categorical(col_data):
        raise ValueError(
            f"facet(): column '{facet_column}' is not categorical. "
            "Faceting requires a categorical column (strings or pandas Categorical)."
        )

    categories = list(dict.fromkeys(col_data))
    n = len(categories)
    cols = min(n, wrap_cols)
    rows = math.ceil(n / cols)

    theme = _resolve_theme(chart._theme_override)

    with theme.as_context():
        fig, axs = plt.subplots(rows, cols, figsize=_facet_figsize(rows, cols))
        axs = np.atleast_2d(np.array(axs)).reshape(rows, cols)

        for i, category in enumerate(categories):
            r, c = divmod(i, cols)
            mask = col_data == category
            sub_adapter = adapter.subset(mask)
            chart._render_onto(fig, axs[r, c], adapter=sub_adapter)
            axs[r, c].set_title(str(category))

        for i in range(n, rows * cols):
            r, c = divmod(i, cols)
            axs[r, c].set_visible(False)

        if chart._title:
            fig.suptitle(chart._title)

        fig.tight_layout()

    return fig, axs


def _facet_figsize(rows, cols, cell_width=4.5, cell_height=3.5):
    """Compute a reasonable figure size from the grid dimensions."""
    return (cols * cell_width, rows * cell_height)
