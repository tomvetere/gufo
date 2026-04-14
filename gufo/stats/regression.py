"""Regression fit overlay for scatter plots."""

from dataclasses import dataclass
from typing import Optional

import numpy as np


@dataclass
class Regression:
    """Configuration for a regression fit line overlaid on a scatter plot.

    Users create instances via gufo.regression(), never directly.
    """

    degree: int = 1
    color: Optional[str] = None
    linestyle: str = "-"
    linewidth: float = 2.0
    label: Optional[str] = None
    n_points: int = 200

    def render(self, x, y, axes):
        """Fit and draw the regression line on the given axes.

        Parameters
        ----------
        x : numpy array — already resolved via DataAdapter.
        y : numpy array — already resolved via DataAdapter.
        axes : matplotlib Axes.
        """
        mask = np.isfinite(x) & np.isfinite(y)
        x_clean, y_clean = x[mask], y[mask]
        if len(x_clean) < self.degree + 1:
            return

        coeffs = np.polyfit(x_clean, y_clean, self.degree)
        x_fit = np.linspace(x_clean.min(), x_clean.max(), self.n_points)
        y_fit = np.polyval(coeffs, x_fit)

        kwargs = {
            "linestyle": self.linestyle,
            "linewidth": self.linewidth,
        }
        if self.color is not None:
            kwargs["color"] = self.color
        if self.label is not None:
            kwargs["label"] = self.label
        else:
            kwargs["label"] = self._auto_label()

        axes.plot(x_fit, y_fit, **kwargs)

    def _auto_label(self):
        if self.degree == 1:
            return "Linear fit"
        return f"Poly({self.degree}) fit"
