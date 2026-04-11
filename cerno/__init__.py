"""
Cerno — data visualization for humans.

"Cerno" (Classical Latin: /ˈker.noː/, KEHR-noh) means
"I discern, I perceive, I distinguish."

A Pythonic, matplotlib-based chart library for researchers,
data explorers, and anyone making reports.
"""

from ._version import __version__
from .core.chart import chart
from .layout.grid import Grid
from .layout.jointplot import jointplot
from .layout.pairplot import pairplot
from .stats.kde import KDE
from .stats.lowess import Lowess
from .stats.regression import Regression
from .style.theme import set_theme, get_theme, register_theme, theme_context


def grid(rows, cols, figsize=None, *, width_ratios=None, height_ratios=None):
    """Create a multi-panel grid layout."""
    return Grid(rows, cols, figsize=figsize,
                width_ratios=width_ratios, height_ratios=height_ratios)


def regression(degree=1, *, color=None, linestyle="-", linewidth=2.0,
               label=None, n_points=200):
    """Create a regression fit configuration for scatter plots."""
    return Regression(
        degree=degree, color=color, linestyle=linestyle,
        linewidth=linewidth, label=label, n_points=n_points,
    )


def kde(*, bw_method=None, color=None, linestyle="-", linewidth=2.0,
        alpha=1.0, label=None, fill=False, n_points=200):
    """Create a KDE configuration for density plots."""
    return KDE(
        bw_method=bw_method, color=color, linestyle=linestyle,
        linewidth=linewidth, alpha=alpha, label=label,
        fill=fill, n_points=n_points,
    )


def lowess(frac=0.6667, *, color=None, linestyle="-", linewidth=2.0,
           label=None):
    """Create a LOWESS smoothing configuration for scatter plots.

    Requires statsmodels. Install with: ``pip install cerno[stats]``.
    """
    return Lowess(
        frac=frac, color=color, linestyle=linestyle,
        linewidth=linewidth, label=label,
    )


__all__ = [
    "__version__",
    "chart",
    "grid",
    "jointplot",
    "pairplot",
    "Grid",
    "set_theme",
    "get_theme",
    "register_theme",
    "theme_context",
    "regression",
    "Regression",
    "kde",
    "KDE",
    "lowess",
    "Lowess",
]
