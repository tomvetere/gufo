"""Chart — the central fluent builder object."""
import matplotlib.pyplot as plt

from ..data.adapter import DataAdapter
from ..layout.facet import render_facet
from ..marks import render_layer
from ..stats.kde import KDE
from ..style.color import resolve_palette
from ..style.theme import _resolve_theme
from .canvas import Canvas
from .layer import Layer


class Chart:
    """
    The main interface for building a gufo chart.

    Methods register layers and options; nothing is drawn until .show() or
    .save() is called. This deferred rendering allows the theme and figure size
    to be finalized before any matplotlib calls are made.

    Users create Chart instances via gufo.chart(), never directly.
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
        self._facet_sharex = True
        self._facet_sharey = True
        self._palette = None
        self._references = []
        self._label_config = None
        self._apply_funcs = []
        self._canvas = Canvas()

    # ------------------------------------------------------------------
    # Mark methods
    # ------------------------------------------------------------------

    def scatter(self, x, y, *, color=None, size=None, alpha=None, label=None,
                cmap=None, vmin=None, vmax=None, colorbar=True,
                fit=None, y_error=None, x_error=None, **kwargs):
        """Add a scatter plot layer.

        y may be a list of column names for wide-form DataFrames — each column
        becomes its own series without requiring pd.melt().

        When color is a numeric column, cmap/vmin/vmax control the colormap
        and range. A colorbar is shown by default (set colorbar=False to hide).

        fit accepts a gufo.regression() config object to overlay a fit line.
        y_error / x_error accept a column name or array for error bars.
        """
        self._layers.append(Layer(
            mark_type="scatter", x=x, y=y,
            encodings={"color": color, "size": size, "alpha": alpha,
                       "label": label, "cmap": cmap, "vmin": vmin,
                       "vmax": vmax, "colorbar": colorbar,
                       "fit": fit,
                       "y_error": y_error, "x_error": x_error},
            kwargs=kwargs,
        ))
        return self

    def line(self, x, y, *, color=None, stroke_dash=None, label=None,
             cmap=None, vmin=None, vmax=None, colorbar=True,
             y_error=None, x_error=None, **kwargs):
        """Add a line plot layer.

        y may be a list of column names for wide-form DataFrames — each column
        becomes its own series without requiring pd.melt().

        When color is a numeric column, the line is drawn as a gradient
        segment-by-segment using cmap/vmin/vmax. A colorbar is shown by
        default (set colorbar=False to hide).

        y_error / x_error accept a column name or array for error bars.
        """
        self._layers.append(Layer(
            mark_type="line", x=x, y=y,
            encodings={"color": color, "stroke_dash": stroke_dash,
                       "label": label, "cmap": cmap, "vmin": vmin,
                       "vmax": vmax, "colorbar": colorbar,
                       "y_error": y_error, "x_error": x_error},
            kwargs=kwargs,
        ))
        return self

    def bar(self, x, y, *, color=None, horizontal=False, stacked=False,
            label=None, y_error=None, x_error=None, **kwargs):
        """Add a bar chart layer.

        y may be a list of column names for wide-form DataFrames — each column
        becomes a grouped bar without requiring pd.melt().

        When color is a categorical column, bars are grouped (dodged) by
        default. Set stacked=True to stack bars instead.

        y_error / x_error accept a column name or array for error bars.
        """
        self._layers.append(Layer(
            mark_type="bar", x=x, y=y,
            encodings={"color": color, "horizontal": horizontal,
                       "stacked": stacked, "label": label,
                       "y_error": y_error, "x_error": x_error},
            kwargs=kwargs,
        ))
        return self

    def histogram(self, x, *, bins="auto", color=None, horizontal=False,
                  label=None, kde=None, **kwargs):
        """Add a histogram layer.

        Set horizontal=True to orient the histogram sideways.
        kde accepts a gufo.kde() config object to overlay a density curve.
        """
        self._layers.append(Layer(
            mark_type="histogram", x=x, y=None,
            encodings={"bins": bins, "color": color, "horizontal": horizontal,
                       "label": label, "kde": kde},
            kwargs=kwargs,
        ))
        return self

    def kde(self, x, *, color=None, bw_method=None, fill=False, label=None,
            **kwargs):
        """Add a KDE (kernel density estimation) layer."""
        kde_config = KDE(bw_method=bw_method, fill=fill)
        self._layers.append(Layer(
            mark_type="kde", x=x, y=None,
            encodings={"color": color, "label": label, "kde_config": kde_config},
            kwargs=kwargs,
        ))
        return self

    def strip(self, x, y, *, color=None, size=None, alpha=None, jitter=0.2,
              horizontal=False, label=None, **kwargs):
        """Add a strip plot layer (jittered points along a categorical axis).

        x is the grouping column (categorical). y is the values column (numeric).

        y may be a list of column names for wide-form DataFrames — each column
        becomes its own strip without requiring pd.melt().
        """
        self._layers.append(Layer(
            mark_type="strip", x=x, y=y,
            encodings={
                "color": color, "size": size, "alpha": alpha,
                "jitter": jitter, "horizontal": horizontal, "label": label,
            },
            kwargs=kwargs,
        ))
        return self

    def swarm(self, x, y, *, color=None, size=None, alpha=None,
              horizontal=False, label=None, **kwargs):
        """Add a swarm plot layer (non-overlapping points along a categorical axis).

        x is the grouping column (categorical). y is the values column (numeric).

        y may be a list of column names for wide-form DataFrames — each column
        becomes its own swarm without requiring pd.melt().
        """
        self._layers.append(Layer(
            mark_type="swarm", x=x, y=y,
            encodings={
                "color": color, "size": size, "alpha": alpha,
                "horizontal": horizontal, "label": label,
            },
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

        - Matrix form: gufo.chart(pivot_df).heatmap() — DataFrame is the matrix.
        - Long-form: gufo.chart(df).heatmap("x", "y", color="value") — pivoted
          internally.
        """
        self._layers.append(Layer(
            mark_type="heatmap", x=x, y=y,
            encodings={"color": color, "cmap": cmap, "annotate": annotate},
            kwargs=kwargs,
        ))
        return self

    def area(self, x, y, *, color=None, alpha=None, label=None,
             y_error=None, **kwargs):
        """Add an area chart layer.

        y may be a list of column names for wide-form DataFrames — each column
        becomes a stacked area without requiring pd.melt().

        y_error accepts a column name or array and draws a lighter error
        band around the top edge of the area (long-form only).
        """
        self._layers.append(Layer(
            mark_type="area", x=x, y=y,
            encodings={"color": color, "alpha": alpha, "label": label,
                       "y_error": y_error},
            kwargs=kwargs,
        ))
        return self

    def countplot(self, x, *, color=None, horizontal=False, label=None, **kwargs):
        """Add a count plot layer — bars showing frequency of each x category."""
        self._layers.append(Layer(
            mark_type="countplot", x=x, y=None,
            encodings={"color": color, "horizontal": horizontal, "label": label},
            kwargs=kwargs,
        ))
        return self

    def ecdf(self, x, *, color=None, label=None, **kwargs):
        """Add an ECDF (empirical cumulative distribution function) layer."""
        self._layers.append(Layer(
            mark_type="ecdf", x=x, y=None,
            encodings={"color": color, "label": label},
            kwargs=kwargs,
        ))
        return self

    def rug(self, x, *, color=None, height=0.05, alpha=0.5, label=None, **kwargs):
        """Add a rug plot layer — tick marks along the x axis."""
        self._layers.append(Layer(
            mark_type="rug", x=x, y=None,
            encodings={"color": color, "height": height, "alpha": alpha,
                       "label": label},
            kwargs=kwargs,
        ))
        return self

    def pointplot(self, x, y, *, color=None, horizontal=False, label=None,
                  **kwargs):
        """Add a point plot layer — connected category means with 95% CI.

        Shows the mean of y for each unique x value, connected by lines,
        with error bars representing the 95% confidence interval (via
        standard error). When color is set, groups are dodged.

        x is the grouping column (categorical). y is the values column
        (numeric).
        """
        self._layers.append(Layer(
            mark_type="pointplot", x=x, y=y,
            encodings={"color": color, "horizontal": horizontal,
                       "label": label},
            kwargs=kwargs,
        ))
        return self

    # ------------------------------------------------------------------
    # Labels and annotations
    # ------------------------------------------------------------------

    def title(self, text):
        """Set the chart title."""
        self._title = text
        return self

    def subtitle(self, text):
        """Set a subtitle displayed below the title in smaller gray text."""
        self._subtitle = text
        return self

    def xlabel(self, text):
        """Set the x-axis label."""
        self._xlabel = text
        return self

    def ylabel(self, text):
        """Set the y-axis label."""
        self._ylabel = text
        return self

    def caption(self, text):
        """Set a caption displayed below the chart in small gray text."""
        self._caption = text
        return self

    def annotate(self, text, xy):
        """Add a text annotation with an arrow pointing to *xy*.

        Parameters
        ----------
        text : str
            The annotation text.
        xy : tuple of float
            The (x, y) data coordinates the arrow points to.
        """
        self._annotations.append({"text": text, "xy": xy})
        return self

    def label(self, column=None, *, fmt=None, fontsize=None, offset=None):
        """Add data labels to bars or scatter points.

        For bar charts, labels are placed at the end of each bar using
        ``axes.bar_label()``. For scatter plots, pass a column name to
        label each point with that column's value.

        Parameters
        ----------
        column : str or None
            Column name whose values label each point (scatter only).
            For bar charts, omit or pass None to label with bar heights.
        fmt : str or None
            Format string (e.g. ``".1f"``, ``".0%"``). For bars, passed
            directly to ``bar_label(fmt=...)``.
        fontsize : int or str or None
            Font size for the labels.
        offset : float or None
            Padding in points between the bar end and the label.
        """
        self._label_config = {
            "column": column, "fmt": fmt,
            "fontsize": fontsize, "offset": offset,
        }
        return self

    # ------------------------------------------------------------------
    # Axis control
    # ------------------------------------------------------------------

    def xlim(self, low, high):
        """Set the x-axis limits."""
        self._xlim = (low, high)
        return self

    def ylim(self, low, high):
        """Set the y-axis limits."""
        self._ylim = (low, high)
        return self

    def xscale(self, scale):
        """Set the x-axis scale (e.g. ``"log"``, ``"symlog"``)."""
        self._xscale = scale
        return self

    def yscale(self, scale):
        """Set the y-axis scale (e.g. ``"log"``, ``"symlog"``)."""
        self._yscale = scale
        return self

    def xticks(self, ticks=None, labels=None, rotation=None):
        """Configure x-axis tick positions, labels, and rotation.

        Parameters
        ----------
        ticks : list or None
            Explicit tick positions.
        labels : list or None
            Labels corresponding to *ticks*.
        rotation : float or None
            Rotation angle in degrees for tick labels.
        """
        self._xticks = {"ticks": ticks, "labels": labels, "rotation": rotation}
        return self

    def yticks(self, ticks=None, labels=None, rotation=None):
        """Configure y-axis tick positions, labels, and rotation.

        Parameters
        ----------
        ticks : list or None
            Explicit tick positions.
        labels : list or None
            Labels corresponding to *ticks*.
        rotation : float or None
            Rotation angle in degrees for tick labels.
        """
        self._yticks = {"ticks": ticks, "labels": labels, "rotation": rotation}
        return self

    # ------------------------------------------------------------------
    # Other chart options
    # ------------------------------------------------------------------

    def legend(self, *, position="best", title=None, hide=False):
        """Configure the legend.

        Parameters
        ----------
        position : str
            Legend location. Any matplotlib loc string (e.g. ``"best"``,
            ``"upper right"``) or one of ``"outside right"``,
            ``"outside left"``, ``"outside top"``, ``"outside bottom"``
            to place the legend outside the axes.
        title : str or None
            Optional legend title.
        hide : bool
            If True, suppress the legend entirely.
        """
        self._legend_opts = {"position": position, "title": title, "hide": hide}
        return self

    def theme(self, name_or_theme):
        """Set the theme for this chart.

        Accepts a theme name (``"gufo_modern"``, ``"gufo_dark"``, etc.)
        or a ``Theme`` instance.
        """
        self._theme_override = name_or_theme
        return self

    def facet(self, column=None, *, row=None, cols=3,
              sharex=True, sharey=True):
        """Split the chart into subplots by one or two categorical columns.

        With column only, panels wrap after cols columns. With row, panels
        form a grid where row categories go down and column categories go
        across. With row only, each row category gets one panel in a
        single column.

        Parameters
        ----------
        column : str or None
            Column for horizontal faceting.
        row : str or None
            Column for vertical faceting.
        cols : int
            Max columns before wrapping (single-variable faceting only).
        sharex : bool
            Share x-axis range across panels. Default True.
        sharey : bool
            Share y-axis range across panels. Default True.
        """
        if self._data is None:
            raise ValueError(
                "facet() requires data bound to the chart. "
                "Pass data to gufo.chart(data)."
            )
        if column is None and row is None:
            raise ValueError(
                "facet() requires at least one of column or row."
            )
        self._facet_column = column
        self._facet_row = row
        self._facet_cols = cols
        self._facet_sharex = sharex
        self._facet_sharey = sharey
        return self

    def apply(self, func):
        """
        Call func(figure, axes) after all layers are rendered.

        func receives the underlying matplotlib Figure and Axes and may call
        any matplotlib method on them. Its return value is ignored. The Chart
        is returned so the chain continues.

        Use this for operations gufo does not yet support natively.
        """
        self._apply_funcs.append(func)
        return self

    def palette(self, colors):
        """Set the color palette for this chart.

        Accepts a list of color strings or a named palette
        ('gufo', 'pastel', 'bold', 'colorblind').
        """
        self._palette = colors
        return self

    # ------------------------------------------------------------------
    # Reference lines and bands
    # ------------------------------------------------------------------

    def hline(self, y, *, color="black", linestyle="--", linewidth=1,
              alpha=0.8, label=None, **kwargs):
        """Add a horizontal reference line."""
        self._references.append(("hline", {"y": y, "color": color,
            "linestyle": linestyle, "linewidth": linewidth, "alpha": alpha,
            "label": label, **kwargs}))
        return self

    def vline(self, x, *, color="black", linestyle="--", linewidth=1,
              alpha=0.8, label=None, **kwargs):
        """Add a vertical reference line."""
        self._references.append(("vline", {"x": x, "color": color,
            "linestyle": linestyle, "linewidth": linewidth, "alpha": alpha,
            "label": label, **kwargs}))
        return self

    def hband(self, y1, y2, *, color="gray", alpha=0.2, label=None, **kwargs):
        """Add a horizontal reference band."""
        self._references.append(("hband", {"y1": y1, "y2": y2, "color": color,
            "alpha": alpha, "label": label, **kwargs}))
        return self

    def vband(self, x1, x2, *, color="gray", alpha=0.2, label=None, **kwargs):
        """Add a vertical reference band."""
        self._references.append(("vband", {"x1": x1, "x2": x2, "color": color,
            "alpha": alpha, "label": label, **kwargs}))
        return self

    def size(self, width, height):
        """Set the figure size in inches as (width, height)."""
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
                                facet_row=self._facet_row,
                                sharex=self._facet_sharex,
                                sharey=self._facet_sharey)

        theme = _resolve_theme(self._theme_override)

        with theme.as_context():
            fig, axes = self._canvas.build()
            self._render_onto(fig, axes)

        return fig, axes

    def _render_onto(self, figure, axes, adapter=None, suppress_legend=False):
        """Render this chart's layers onto an externally provided axes.

        Used by Grid and facet rendering. When adapter is provided, it is
        used instead of creating one from self._data. When suppress_legend
        is True, the per-axes legend is skipped — facet rendering uses this
        to draw a single figure-level legend after all panels are rendered.
        """
        theme = _resolve_theme(self._theme_override)
        if adapter is None:
            adapter = DataAdapter.from_any(self._data)

        resolved_palette = resolve_palette(self._palette)

        with theme.as_context():
            for layer in self._layers:
                layer.palette = resolved_palette
                render_layer(layer, adapter, axes)
            self._apply_decorators(figure, axes, adapter,
                                   suppress_legend=suppress_legend)
            for func in self._apply_funcs:
                func(figure, axes)

    def _apply_decorators(self, fig, axes, adapter=None, suppress_legend=False):
        for attr, method in self._SIMPLE_SETTERS:
            value = getattr(self, attr)
            if value is not None:
                getattr(axes, method)(value)

        if self._xlim:
            axes.set_xlim(*self._xlim)
        if self._ylim:
            axes.set_ylim(*self._ylim)

        self._apply_labels(axes, adapter)
        self._apply_references(axes)
        self._apply_subtitle(fig)
        self._apply_caption(fig)
        self._apply_ticks(axes, "x", self._xticks)
        self._apply_ticks(axes, "y", self._yticks)
        self._apply_annotations(axes)
        if not suppress_legend:
            self._apply_legend(axes)

    def _apply_labels(self, axes, adapter=None):
        if not self._label_config:
            return

        mark_types = {layer.mark_type for layer in self._layers}
        line_only = bool(mark_types & {"line", "pointplot"}) and not (
            mark_types & {"bar", "countplot", "scatter"}
        )

        if line_only:
            self._label_line_points(axes, adapter)
            return

        if axes.containers:
            self._label_bar_containers(axes)
            return

        if self._label_config.get("column") is not None:
            self._label_scatter_offsets(axes, adapter)

    def _label_text_kwargs(self):
        """Return (annotate_kwargs, text_offset) from the label config."""
        cfg = self._label_config
        kw = {}
        if cfg.get("fontsize") is not None:
            kw["fontsize"] = cfg["fontsize"]
        offset = cfg.get("offset")
        return kw, offset if offset is not None else 5

    def _label_bar_containers(self, axes):
        cfg = self._label_config
        kw, _ = self._label_text_kwargs()
        fmt = cfg.get("fmt")
        if fmt is not None:
            kw["fmt"] = f"%{fmt}"
        if cfg.get("offset") is not None:
            kw["padding"] = cfg["offset"]
        for container in axes.containers:
            axes.bar_label(container, **kw)

    def _label_scatter_offsets(self, axes, adapter):
        column = self._label_config.get("column")
        if adapter is None:
            adapter = DataAdapter.from_any(self._data)
        labels = adapter.resolve(column)
        kw, text_offset = self._label_text_kwargs()
        for collection in axes.collections:
            offsets = collection.get_offsets()
            if len(offsets) == len(labels):
                for (px, py), lbl in zip(offsets, labels):
                    axes.annotate(str(lbl), (px, py),
                                  textcoords="offset points",
                                  xytext=(0, text_offset),
                                  ha="center", **kw)
                break

    def _label_line_points(self, axes, adapter):
        """Label each point on a line or pointplot mark.

        If a column is configured, its values are used as labels; otherwise
        the y-values are formatted via *fmt* (default two decimals).
        """
        data_lines = [ln for ln in axes.lines if len(ln.get_xdata()) > 0]
        if not data_lines:
            return
        cfg = self._label_config
        column = cfg.get("column")
        fmt = cfg.get("fmt")

        line = data_lines[0]
        xs = line.get_xdata()
        ys = line.get_ydata()

        if column is not None:
            if adapter is None:
                adapter = DataAdapter.from_any(self._data)
            labels = adapter.resolve(column)
            if len(labels) != len(xs):
                return
            text_values = [str(lbl) for lbl in labels]
        else:
            fmt_str = "{:" + fmt + "}" if fmt else "{:.2f}"
            text_values = [fmt_str.format(y) for y in ys]

        kw, text_offset = self._label_text_kwargs()
        for px, py, lbl in zip(xs, ys, text_values):
            axes.annotate(lbl, (px, py),
                          textcoords="offset points",
                          xytext=(0, text_offset),
                          ha="center", **kw)

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

    def _apply_references(self, axes):
        for kind, opts in self._references:
            kw = {k: v for k, v in opts.items() if v is not None}
            if kind == "hline":
                axes.axhline(kw.pop("y"), **kw)
            elif kind == "vline":
                axes.axvline(kw.pop("x"), **kw)
            elif kind == "hband":
                axes.axhspan(kw.pop("y1"), kw.pop("y2"), **kw)
            elif kind == "vband":
                axes.axvspan(kw.pop("x1"), kw.pop("x2"), **kw)

    _OUTSIDE_LEGEND = {
        "outside right": {"bbox_to_anchor": (1.02, 0.5), "loc": "center left"},
        "outside left": {"bbox_to_anchor": (-0.02, 0.5), "loc": "center right"},
        "outside top": {"bbox_to_anchor": (0.5, 1.12), "loc": "lower center"},
        "outside bottom": {"bbox_to_anchor": (0.5, -0.12), "loc": "upper center"},
    }

    def _apply_legend(self, axes):
        if not self._legend_opts:
            return
        if self._legend_opts.get("hide"):
            return
        position = self._legend_opts.get("position", "best")
        title = self._legend_opts.get("title")
        outside = self._OUTSIDE_LEGEND.get(position)
        if outside is not None:
            axes.legend(title=title, **outside)
        else:
            axes.legend(loc=position, title=title)


def chart(data=None):
    """Create a new Chart. The entry point for all gufo charts."""
    return Chart(data)
