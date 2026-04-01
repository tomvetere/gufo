"""Chart — the central fluent builder object."""
from .canvas import Canvas
from .layer import Layer


class Chart:
    """
    The main interface for building a cerno chart.

    Methods register layers and options; nothing is drawn until .show() or
    .save() is called. This deferred rendering allows the theme and figure size
    to be finalized before any matplotlib calls are made.

    Users create Chart instances via cerno.chart(), never directly.
    """

    def __init__(self, data=None):
        self._data = data
        self._layers = []
        self._title = None
        self._subtitle = None
        self._xlabel = None
        self._ylabel = None
        self._caption = None
        self._annotations = []
        self._xlim = None
        self._ylim = None
        self._xscale = None
        self._yscale = None
        self._xticks = {}
        self._yticks = {}
        self._legend_opts = None
        self._theme_override = None
        self._facet_opts = None
        self._apply_funcs = []
        self._canvas = Canvas()

    # ------------------------------------------------------------------
    # Mark methods
    # ------------------------------------------------------------------

    def scatter(self, x, y, *, color=None, size=None, alpha=None, label=None, **kwargs):
        """Add a scatter plot layer."""
        self._layers.append(Layer(
            mark_type="scatter", x=x, y=y,
            encodings={"color": color, "size": size, "alpha": alpha, "label": label},
            kwargs=kwargs,
        ))
        return self

    def line(self, x, y, *, color=None, stroke_dash=None, label=None, **kwargs):
        """
        Add a line plot layer.

        y may be a list of column names for wide-form DataFrames — each column
        becomes its own series without requiring pd.melt().
        """
        self._layers.append(Layer(
            mark_type="line", x=x, y=y,
            encodings={"color": color, "stroke_dash": stroke_dash, "label": label},
            kwargs=kwargs,
        ))
        return self

    def bar(self, x, y, *, color=None, horizontal=False, label=None, **kwargs):
        """Add a bar chart layer."""
        self._layers.append(Layer(
            mark_type="bar", x=x, y=y,
            encodings={"color": color, "horizontal": horizontal, "label": label},
            kwargs=kwargs,
        ))
        return self

    def histogram(self, x, *, bins="auto", color=None, label=None, **kwargs):
        """Add a histogram layer."""
        self._layers.append(Layer(
            mark_type="histogram", x=x, y=None,
            encodings={"bins": bins, "color": color, "label": label},
            kwargs=kwargs,
        ))
        return self

    # ------------------------------------------------------------------
    # Labels and annotations
    # ------------------------------------------------------------------

    def title(self, text):
        self._title = text
        return self

    def subtitle(self, text):
        self._subtitle = text
        return self

    def xlabel(self, text):
        self._xlabel = text
        return self

    def ylabel(self, text):
        self._ylabel = text
        return self

    def caption(self, text):
        self._caption = text
        return self

    def annotate(self, text, xy):
        self._annotations.append({"text": text, "xy": xy})
        return self

    # ------------------------------------------------------------------
    # Axis control
    # ------------------------------------------------------------------

    def xlim(self, low, high):
        self._xlim = (low, high)
        return self

    def ylim(self, low, high):
        self._ylim = (low, high)
        return self

    def xscale(self, scale):
        self._xscale = scale
        return self

    def yscale(self, scale):
        self._yscale = scale
        return self

    def xticks(self, ticks=None, labels=None, rotation=None):
        self._xticks = {"ticks": ticks, "labels": labels, "rotation": rotation}
        return self

    def yticks(self, ticks=None, labels=None, rotation=None):
        self._yticks = {"ticks": ticks, "labels": labels, "rotation": rotation}
        return self

    # ------------------------------------------------------------------
    # Other chart options
    # ------------------------------------------------------------------

    def legend(self, *, position="best", title=None, hide=False):
        self._legend_opts = {"position": position, "title": title, "hide": hide}
        return self

    def theme(self, name_or_theme):
        self._theme_override = name_or_theme
        return self

    def facet(self, col=None, row=None, *, cols=3):
        self._facet_opts = {"col": col, "row": row, "cols": cols}
        return self

    def apply(self, func):
        """
        Call func(figure, axes) after all layers are rendered.

        func receives the underlying matplotlib Figure and Axes and may call
        any matplotlib method on them. Its return value is ignored. The Chart
        is returned so the chain continues.

        Use this for operations cerno does not yet support natively.
        """
        self._apply_funcs.append(func)
        return self

    def size(self, width, height):
        self._canvas = Canvas(figsize=(width, height))
        return self

    # ------------------------------------------------------------------
    # Output
    # ------------------------------------------------------------------

    def show(self):
        """Render and display the chart."""
        fig, axes = self._render()
        import matplotlib.pyplot as plt
        plt.show()
        return self

    def save(self, path, *, dpi=150):
        """Render and save the chart to a file."""
        fig, axes = self._render()
        fig.savefig(path, dpi=dpi, bbox_inches="tight")
        return self

    # ------------------------------------------------------------------
    # Internal rendering pipeline
    # ------------------------------------------------------------------

    def _render(self):
        """
        Build the figure and draw all registered layers.

        Rendering order:
        1. Resolve theme (override or global)
        2. Create figure / axes via Canvas
        3. Draw each Layer via the appropriate Mark
        4. Apply decorators (title, labels, axis options, legend)
        5. Call each .apply() function
        """
        from ..style.theme import _resolve_theme
        from ..marks import render_layer

        theme = _resolve_theme(self._theme_override)

        with theme.as_context():
            fig, axes = self._canvas.build()

            for layer in self._layers:
                render_layer(layer, self._data, axes)

            self._apply_decorators(fig, axes)

            for func in self._apply_funcs:
                func(fig, axes)

        return fig, axes

    def _apply_decorators(self, fig, axes):
        if self._title:
            axes.set_title(self._title)
        if self._subtitle:
            fig.text(0.5, 0.92, self._subtitle, ha="center", fontsize="medium",
                     color="gray", transform=fig.transFigure)
        if self._xlabel:
            axes.set_xlabel(self._xlabel)
        if self._ylabel:
            axes.set_ylabel(self._ylabel)
        if self._caption:
            fig.text(0.5, 0.01, self._caption, ha="center", fontsize="small",
                     color="gray", transform=fig.transFigure)
        if self._xlim:
            axes.set_xlim(*self._xlim)
        if self._ylim:
            axes.set_ylim(*self._ylim)
        if self._xscale:
            axes.set_xscale(self._xscale)
        if self._yscale:
            axes.set_yscale(self._yscale)
        if self._xticks:
            opts = self._xticks
            if opts.get("ticks") is not None:
                axes.set_xticks(opts["ticks"])
            if opts.get("labels") is not None:
                axes.set_xticklabels(opts["labels"])
            if opts.get("rotation") is not None:
                axes.tick_params(axis="x", labelrotation=opts["rotation"])
        if self._yticks:
            opts = self._yticks
            if opts.get("ticks") is not None:
                axes.set_yticks(opts["ticks"])
            if opts.get("labels") is not None:
                axes.set_yticklabels(opts["labels"])
            if opts.get("rotation") is not None:
                axes.tick_params(axis="y", labelrotation=opts["rotation"])
        if self._annotations:
            for ann in self._annotations:
                axes.annotate(ann["text"], xy=ann["xy"],
                              xytext=(15, 15), textcoords="offset points",
                              arrowprops={"arrowstyle": "->", "color": "black"})
        if self._legend_opts:
            opts = self._legend_opts
            if not opts.get("hide"):
                axes.legend(loc=opts.get("position", "best"),
                            title=opts.get("title"))


def chart(data=None):
    """Create a new Chart. The entry point for all cerno charts."""
    return Chart(data)
