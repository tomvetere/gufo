"""Chart — the central fluent builder object."""
import matplotlib.pyplot as plt

from ..data.adapter import DataAdapter
from ..layout.facet import render_facet
from ..marks import render_layer
from ..style.theme import _resolve_theme
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

    _SIMPLE_SETTERS = [
        ("_title", "set_title"),
        ("_xlabel", "set_xlabel"),
        ("_ylabel", "set_ylabel"),
        ("_xscale", "set_xscale"),
        ("_yscale", "set_yscale"),
    ]

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
        self._facet_column = None
        self._facet_row = None
        self._facet_cols = None
        self._apply_funcs = []
        self._canvas = Canvas()

    # ------------------------------------------------------------------
    # Mark methods
    # ------------------------------------------------------------------

    def scatter(self, x, y, *, color=None, size=None, alpha=None, label=None, **kwargs):
        """Add a scatter plot layer.

        y may be a list of column names for wide-form DataFrames — each column
        becomes its own series without requiring pd.melt().
        """
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
        """Add a bar chart layer.

        y may be a list of column names for wide-form DataFrames — each column
        becomes a grouped bar without requiring pd.melt().
        """
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

    def boxplot(self, x, y, *, color=None, horizontal=False, label=None, **kwargs):
        """Add a box plot layer.

        x is the grouping column (categorical). y is the values column (numeric).
        Each unique x value produces one box.

        y may be a list of column names for wide-form DataFrames — each column
        becomes its own box without requiring pd.melt().
        """
        self._layers.append(Layer(
            mark_type="boxplot", x=x, y=y,
            encodings={"color": color, "horizontal": horizontal, "label": label},
            kwargs=kwargs,
        ))
        return self

    def violin(self, x, y, *, color=None, horizontal=False, label=None, **kwargs):
        """Add a violin plot layer.

        x is the grouping column (categorical). y is the values column (numeric).
        Each unique x value produces one violin.

        y may be a list of column names for wide-form DataFrames — each column
        becomes its own violin without requiring pd.melt().
        """
        self._layers.append(Layer(
            mark_type="violin", x=x, y=y,
            encodings={"color": color, "horizontal": horizontal, "label": label},
            kwargs=kwargs,
        ))
        return self

    def heatmap(self, x=None, y=None, *, color=None, cmap=None, annotate=False, **kwargs):
        """Add a heatmap layer.

        Two usage modes:
        - Matrix form: cerno.chart(pivot_df).heatmap() — DataFrame is the matrix.
        - Long-form: cerno.chart(df).heatmap("x", "y", color="value") — pivoted
          internally.
        """
        self._layers.append(Layer(
            mark_type="heatmap", x=x, y=y,
            encodings={"color": color, "cmap": cmap, "annotate": annotate},
            kwargs=kwargs,
        ))
        return self

    def area(self, x, y, *, color=None, alpha=None, label=None, **kwargs):
        """Add an area chart layer.

        y may be a list of column names for wide-form DataFrames — each column
        becomes a stacked area without requiring pd.melt().
        """
        self._layers.append(Layer(
            mark_type="area", x=x, y=y,
            encodings={"color": color, "alpha": alpha, "label": label},
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

    def facet(self, column=None, *, row=None, cols=3):
        """Split the chart into subplots by one or two categorical columns.

        With column only, panels wrap after cols columns. With row, panels
        form a grid where row categories go down and column categories go
        across. With row only, each row category gets one panel in a
        single column.
        """
        if self._data is None:
            raise ValueError(
                "facet() requires data bound to the chart. "
                "Pass data to cerno.chart(data)."
            )
        if column is None and row is None:
            raise ValueError(
                "facet() requires at least one of column or row."
            )
        self._facet_column = column
        self._facet_row = row
        self._facet_cols = cols
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
        plt.show()
        return self

    def save(self, path, *, dpi=150):
        """Render and save the chart to a file."""
        fig, axes = self._render()
        fig.savefig(path, dpi=dpi, bbox_inches="tight")
        plt.close(fig)
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
        if self._facet_column is not None or self._facet_row is not None:
            return render_facet(self, self._facet_column, self._facet_cols,
                                facet_row=self._facet_row)

        theme = _resolve_theme(self._theme_override)
        adapter = DataAdapter.from_any(self._data)

        with theme.as_context():
            fig, axes = self._canvas.build()

            for layer in self._layers:
                render_layer(layer, adapter, axes)

            self._apply_decorators(fig, axes)

            for func in self._apply_funcs:
                func(fig, axes)

        return fig, axes

    def _render_onto(self, figure, axes, adapter=None):
        """Render this chart's layers onto an externally provided axes.

        Used by Grid and facet rendering. When adapter is provided, it is
        used instead of creating one from self._data.
        """
        theme = _resolve_theme(self._theme_override)
        if adapter is None:
            adapter = DataAdapter.from_any(self._data)

        with theme.as_context():
            for layer in self._layers:
                render_layer(layer, adapter, axes)
            self._apply_decorators(figure, axes)
            for func in self._apply_funcs:
                func(figure, axes)

    def _apply_decorators(self, fig, axes):
        for attr, method in self._SIMPLE_SETTERS:
            value = getattr(self, attr)
            if value is not None:
                getattr(axes, method)(value)

        if self._xlim:
            axes.set_xlim(*self._xlim)
        if self._ylim:
            axes.set_ylim(*self._ylim)

        self._apply_subtitle(fig)
        self._apply_caption(fig)
        self._apply_ticks(axes, "x", self._xticks)
        self._apply_ticks(axes, "y", self._yticks)
        self._apply_annotations(axes)
        self._apply_legend(axes)

    def _apply_subtitle(self, fig):
        if self._subtitle:
            fig.text(0.5, 0.92, self._subtitle, ha="center", fontsize="medium",
                     color="gray", transform=fig.transFigure)

    def _apply_caption(self, fig):
        if self._caption:
            fig.text(0.5, 0.01, self._caption, ha="center", fontsize="small",
                     color="gray", transform=fig.transFigure)

    def _apply_ticks(self, axes, axis, opts):
        if not opts:
            return
        if opts.get("ticks") is not None:
            getattr(axes, f"set_{axis}ticks")(opts["ticks"])
        if opts.get("labels") is not None:
            getattr(axes, f"set_{axis}ticklabels")(opts["labels"])
        if opts.get("rotation") is not None:
            axes.tick_params(axis=axis, labelrotation=opts["rotation"])

    def _apply_annotations(self, axes):
        for ann in self._annotations:
            axes.annotate(ann["text"], xy=ann["xy"],
                          xytext=(15, 15), textcoords="offset points",
                          arrowprops={"arrowstyle": "->", "color": "black"})

    def _apply_legend(self, axes):
        if not self._legend_opts:
            return
        if not self._legend_opts.get("hide"):
            axes.legend(loc=self._legend_opts.get("position", "best"),
                        title=self._legend_opts.get("title"))


def chart(data=None):
    """Create a new Chart. The entry point for all cerno charts."""
    return Chart(data)
