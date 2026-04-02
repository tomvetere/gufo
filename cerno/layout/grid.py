"""Grid — programmer-controlled multi-panel layout."""
import matplotlib.pyplot as plt
from ..core.chart import Chart


class GridCell:
    """A single cell in a Grid, exposing .chart() to bind data."""

    def __init__(self, axes):
        self._axes = axes

    def chart(self, data=None):
        """Return a Chart bound to this cell's axes."""
        ch = Chart(data)
        ch._canvas._axes = self._axes
        ch._canvas._figure = self._axes.figure
        ch._canvas._built = True
        return ch


class Grid:
    """
    A fixed rows×cols grid of panels.

    Usage::

        g = cerno.grid(2, 2, figsize=(14, 10))
        g[0, 0].chart(df).scatter("x", "y").title("Top Left")
        g[0, 1].chart(df).line("x", "y").title("Top Right")
        g.show()
    """

    def __init__(self, rows, cols, figsize=None):
        self._fig, self._axs = plt.subplots(rows, cols, figsize=figsize)
        import numpy as np
        self._axs = np.atleast_2d(np.array(self._axs)).reshape(rows, cols)

    def __getitem__(self, idx):
        return GridCell(self._axs[idx])

    def show(self):
        self._fig.tight_layout()
        plt.show()

    def save(self, path, *, dpi=150):
        self._fig.tight_layout()
        self._fig.savefig(path, dpi=dpi, bbox_inches="tight")


def grid(rows, cols, figsize=None):
    """Create a multi-panel grid layout."""
    return Grid(rows, cols, figsize=figsize)
