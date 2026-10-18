"""Kernel Density Estimation — standalone mark and histogram overlay."""

import warnings
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

    Used as an overlay on .histogram() via histogram(kde=gufo.kde(...)).
    For a standalone density plot, use Chart.kdeplot() instead.

    Users create instances via gufo.kde(), never directly.
    """

    bw_method: Optional[object] = None
    color: Optional[str] = None
    linestyle: str = "-"
    linewidth: float = 2.0
    alpha: float = 1.0
    label: Optional[str] = None
    fill: bool = False
    n_points: int = 200

    def render(self, x, axes, *, scale_to_hist=False, hist_patches=None,
               **extra_kwargs):
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
        \**extra_kwargs
            Additional keyword arguments passed through to matplotlib.
        """
        scale = 1.0
        if scale_to_hist and hist_patches is not None:
            bin_width = hist_patches[0].get_width() if hist_patches else 1.0
            scale = np.isfinite(x).sum() * bin_width
        self._render(x, axes, scale=scale, **extra_kwargs)

    def _render(self, x, axes, *, scale=1.0, horizontal=False,
                **extra_kwargs):
        """Draw the KDE curve, multiplied by ``scale``.

        A histogram overlay passes the area of its bars as ``scale``, so the
        curve (area 1) is drawn in the histogram's units.
        """
        _require_scipy("KDE")

        x_clean = x[np.isfinite(x)]
        if len(x_clean) < 2:
            return

        if np.ptp(x_clean) == 0:
            warnings.warn(
                f"KDE: all {len(x_clean)} values equal {x_clean[0]:g}, so "
                "there is no density to draw; the curve is skipped.",
                stacklevel=2,
            )
            return

        kernel = gaussian_kde(x_clean, bw_method=self.bw_method)
        x_grid = np.linspace(x_clean.min(), x_clean.max(), self.n_points)
        density = kernel(x_grid) * scale

        kwargs = {
            "linestyle": self.linestyle,
            "linewidth": self.linewidth,
            "alpha": self.alpha,
            **extra_kwargs,
        }
        if self.color is not None:
            kwargs["color"] = self.color
        if self.label is not None:
            kwargs["label"] = self.label
        else:
            kwargs["label"] = "KDE"

        if self.fill and horizontal:
            axes.fill_betweenx(x_grid, density, **kwargs)
        elif self.fill:
            axes.fill_between(x_grid, density, **kwargs)
        elif horizontal:
            axes.plot(density, x_grid, **kwargs)
        else:
            axes.plot(x_grid, density, **kwargs)
