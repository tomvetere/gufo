"""LOWESS smoothing overlay for scatter plots."""

from dataclasses import dataclass
from typing import Optional

import numpy as np

try:
    from statsmodels.nonparametric.smoothers_lowess import lowess as sm_lowess
except ImportError:
    sm_lowess = None


@dataclass
class Lowess:
    """Configuration for a LOWESS smoothing curve overlaid on a scatter plot.

    Users create instances via gufo.lowess(), never directly.
    """

    frac: float = 0.6667
    color: Optional[str] = None
    linestyle: str = "-"
    linewidth: float = 2.0
    label: Optional[str] = None

    def render(self, x, y, axes):
        """Fit and draw the LOWESS curve on the given axes.

        Parameters
        ----------
        x : numpy array — already resolved via DataAdapter.
        y : numpy array — already resolved via DataAdapter.
        axes : matplotlib Axes.
        """
        if sm_lowess is None:
            raise ImportError(
                "LOWESS smoothing requires statsmodels. "
                "Install it with: pip install gufo[stats]"
            )

        mask = np.isfinite(x) & np.isfinite(y)
        x_clean, y_clean = x[mask], y[mask]
        if len(x_clean) < 3:
            return

        result = sm_lowess(y_clean, x_clean, frac=self.frac,
                           return_sorted=True)
        x_fit, y_fit = result[:, 0], result[:, 1]

        kwargs = {
            "linestyle": self.linestyle,
            "linewidth": self.linewidth,
        }
        if self.color is not None:
            kwargs["color"] = self.color
        if self.label is not None:
            kwargs["label"] = self.label

        axes.plot(x_fit, y_fit, **kwargs)
