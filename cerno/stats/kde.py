"""Kernel Density Estimation — standalone mark and histogram overlay."""

from dataclasses import dataclass
from typing import Optional

import numpy as np

try:
    from scipy.stats import gaussian_kde
except ImportError:
    gaussian_kde = None

from . import _require_scipy


@dataclass
class KDE:
    """Configuration for a KDE curve.

    Used both as a standalone mark via .kde() and as an overlay
    parameter on .histogram(kde=cerno.kde()).

    Users create instances via cerno.kde(), never directly.
    """

    bw_method: Optional[object] = None
    color: Optional[str] = None
    linestyle: str = "-"
    linewidth: float = 2.0
    alpha: float = 1.0
    label: Optional[str] = None
    fill: bool = False
    n_points: int = 200

    def render(self, x, axes, *, scale_to_hist=False, hist_patches=None):
        """Compute and draw the KDE curve.

        Parameters
        ----------
        x : numpy array
            The data to estimate density for.
        axes : matplotlib Axes
            Target axes to draw on.
        scale_to_hist : bool
            If True, scale the KDE to match histogram bar heights.
        hist_patches : list or None
            Patches from axes.hist(), used for bin width when scaling.
        """
        _require_scipy("KDE")

        x_clean = x[np.isfinite(x)]
        if len(x_clean) < 2:
            return

        kernel = gaussian_kde(x_clean, bw_method=self.bw_method)
        x_grid = np.linspace(x_clean.min(), x_clean.max(), self.n_points)
        density = kernel(x_grid)

        if scale_to_hist and hist_patches is not None:
            bin_width = hist_patches[0].get_width() if hist_patches else 1.0
            density = density * len(x_clean) * bin_width

        kwargs = {
            "linestyle": self.linestyle,
            "linewidth": self.linewidth,
            "alpha": self.alpha,
        }
        if self.color is not None:
            kwargs["color"] = self.color
        if self.label is not None:
            kwargs["label"] = self.label
        else:
            kwargs["label"] = "KDE"

        if self.fill:
            axes.fill_between(x_grid, density, **kwargs)
        else:
            axes.plot(x_grid, density, **kwargs)
