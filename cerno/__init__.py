"""
Cerno — data visualization for humans.

A Pythonic, matplotlib-based chart library for researchers,
data explorers, and anyone making reports.
"""

from ._version import __version__
from .core.chart import chart
from .layout.grid import Grid
from .style.theme import set_theme, get_theme, register_theme, theme_context


def grid(rows, cols, figsize=None):
    """Create a multi-panel grid layout."""
    return Grid(rows, cols, figsize=figsize)


__all__ = [
    "__version__",
    "chart",
    "grid",
    "Grid",
    "set_theme",
    "get_theme",
    "register_theme",
    "theme_context",
]
