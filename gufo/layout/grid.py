"""Grid — multi-panel layout container for Chart objects."""
import matplotlib.pyplot as plt
import numpy as np

from ..core.chart import Chart
from ..style.theme import _resolve_theme


class Grid:
    """
    A layout container that arranges multiple Charts in a grid.

    Users create Grid instances via gufo.grid(), never directly.
    Panels are assigned with g[row, col] = gufo.chart(data).mark(...).
    """

    def __init__(self, rows, cols, figsize=None, *,
                 width_ratios=None, height_ratios=None):
        self._rows = rows
        self._cols = cols
        self._figsize = figsize
        self._width_ratios = width_ratios
        self._height_ratios = height_ratios
        self._panels = {}
        self._title = None
        self._theme_override = None
        self._apply_funcs = []

    def __setitem__(self, idx, panel_chart):
        if not isinstance(panel_chart, Chart):
            raise TypeError("Panel must be a Chart instance.")
        r, c = idx
        if not (0 <= r < self._rows and 0 <= c < self._cols):
            raise IndexError(
                f"Index {idx} out of range for {self._rows}x{self._cols} grid."
            )
        self._panels[idx] = panel_chart

    def __getitem__(self, idx):
        raise TypeError(
            "Grid cells are write-only. "
            "Use: g[0, 0] = gufo.chart(df).scatter('x', 'y')"
        )

    def title(self, text):
        """Set the overall grid title (displayed above all panels)."""
        self._title = text
        return self

    def theme(self, name_or_theme):
        """Set the theme for the entire grid.

        Accepts a theme name or a ``Theme`` instance.
        """
        self._theme_override = name_or_theme
        return self

    def apply(self, func):
        """
        Call func(figure, axes) after all panels are rendered.

        func receives the matplotlib Figure and the 2D numpy array of Axes.
        Its return value is ignored. The Grid is returned so the chain continues.
        """
        self._apply_funcs.append(func)
        return self

    def show(self):
        """Render and display the grid."""
        self._render()
        plt.show()
        return self

    def save(self, path, *, dpi=150):
        """Render and save the grid to a file."""
        fig, _ = self._render()
        fig.savefig(path, dpi=dpi, bbox_inches="tight")
        plt.close(fig)
        return self

    def _render(self):
        theme = _resolve_theme(self._theme_override)

        with theme.as_context():
            gridspec_kw = {}
            if self._width_ratios is not None:
                gridspec_kw["width_ratios"] = self._width_ratios
            if self._height_ratios is not None:
                gridspec_kw["height_ratios"] = self._height_ratios
            fig, axs = plt.subplots(
                self._rows, self._cols, figsize=self._figsize,
                gridspec_kw=gridspec_kw or None,
            )
            axs = np.atleast_2d(np.array(axs)).reshape(self._rows, self._cols)

            assigned = set()
            for (r, c), panel in self._panels.items():
                assigned.add((r, c))
                panel._render_onto(fig, axs[r, c])

            for r in range(self._rows):
                for c in range(self._cols):
                    if (r, c) not in assigned:
                        axs[r, c].set_visible(False)

            if self._title:
                fig.suptitle(self._title)

            fig.tight_layout()

            for func in self._apply_funcs:
                func(fig, axs)

        return fig, axs
