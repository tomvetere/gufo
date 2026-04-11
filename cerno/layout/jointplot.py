"""Joint plot — scatter with marginal distributions on edges."""
from ..core.chart import chart
from ..layout.grid import Grid

_VALID_MARGINALS = ("histogram", "kde")


def jointplot(data, x, y, *, color=None, marginal="histogram", figsize=None):
    """Create a joint plot with marginal distributions.

    Shows a central scatter plot with a marginal distribution (histogram
    or KDE) on the top and right edges.

    Parameters
    ----------
    data : DataFrame, dict, or similar
        The data source.
    x : str
        Column name for the horizontal axis.
    y : str
        Column name for the vertical axis.
    color : str or None
        Column name for categorical color encoding.
    marginal : str
        Type of marginal plot: ``"histogram"`` (default) or ``"kde"``.
    figsize : tuple or None
        Figure size as (width, height). Defaults to (8, 8).

    Returns
    -------
    Grid
        A Grid instance ready for ``.show()`` or ``.save()``.
    """
    if marginal not in _VALID_MARGINALS:
        raise ValueError(
            f"marginal must be one of {_VALID_MARGINALS}, got {marginal!r}."
        )

    if figsize is None:
        figsize = (8, 8)

    g = Grid(2, 2, figsize=figsize,
             width_ratios=[4, 1], height_ratios=[1, 4])

    g[1, 0] = chart(data).scatter(x, y, color=color).xlabel(x).ylabel(y)
    g[0, 0] = _marginal_chart(data, x, color=color, marginal=marginal)
    g[1, 1] = _marginal_chart(data, y, color=color, marginal=marginal,
                               horizontal=True)

    g.apply(_clean_marginals)

    return g


def _marginal_chart(data, col, *, color, marginal, horizontal=False):
    """Build a marginal distribution chart (histogram or KDE)."""
    if marginal == "kde":
        return chart(data).kde(col, color=color)
    return chart(data).histogram(col, color=color, horizontal=horizontal)


def _clean_marginals(fig, axs):
    """Hide labels and tick labels on marginal axes."""
    top = axs[0, 0]
    right = axs[1, 1]

    top.set_xlabel("")
    top.set_ylabel("")
    top.tick_params(labelbottom=False)

    right.set_xlabel("")
    right.set_ylabel("")
    right.tick_params(labelleft=False)
