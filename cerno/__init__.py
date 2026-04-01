"""
Cerno — data visualization for humans.

A Pythonic, matplotlib-based chart library for researchers,
data explorers, and anyone making reports.
"""

from ._version import __version__
from .core.chart import chart
from .style.theme import set_theme, get_theme, register_theme, theme_context
from .layout.grid import grid

__all__ = [
    "__version__",
    "chart",
    "set_theme",
    "get_theme",
    "register_theme",
    "theme_context",
    "grid",
]
