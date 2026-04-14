"""Pair plot — NxN grid of scatter plots and histograms for variable pairs."""
from ..core.chart import chart
from ..data.adapter import DataAdapter
from ..data.inference import is_categorical
from ..layout.grid import Grid


def pairplot(data, columns=None, *, color=None, figsize=None):
    """Create a pair plot grid from columnar data.

    Generates an NxN grid where diagonal cells show histograms and
    off-diagonal cells show scatter plots for every pair of numeric
    columns.

    Parameters
    ----------
    data : DataFrame, dict, or similar
        The data source. Must have named columns.
    columns : list of str or None
        Which columns to include. If None, all numeric columns are
        used automatically.
    color : str or None
        Column name for categorical color encoding. Applied to all
        panels.
    figsize : tuple or None
        Figure size as (width, height). Defaults to (n*3, n*3).

    Returns
    -------
    Grid
        A Grid instance ready for .show() or .save().
    """
    adapter = DataAdapter.from_any(data)

    if columns is None:
        columns = _detect_numeric_columns(adapter, exclude=color)

    if len(columns) < 2:
        raise ValueError(
            "pairplot() requires at least 2 numeric columns, "
            f"but found {len(columns)}."
        )

    n = len(columns)
    if figsize is None:
        figsize = (n * 3, n * 3)

    g = Grid(n, n, figsize=figsize)

    for i in range(n):
        for j in range(n):
            if i == j:
                panel = chart(data).histogram(columns[i], color=color)
            else:
                panel = chart(data).scatter(
                    columns[j], columns[i], color=color, alpha=0.5,
                )

            if i == n - 1:
                panel.xlabel(columns[j])
            if j == 0:
                panel.ylabel(columns[i])

            g[i, j] = panel

    return g


def _detect_numeric_columns(adapter, exclude=None):
    """Return column names whose resolved arrays are numeric."""
    numeric = []
    for name in adapter.column_names():
        if name == exclude:
            continue
        arr = adapter.resolve(name)
        if not is_categorical(arr):
            numeric.append(name)
    return numeric
