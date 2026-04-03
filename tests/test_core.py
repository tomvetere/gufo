"""Tests for cerno.core — Chart, Layer, Canvas."""
import numpy as np
import pytest

import cerno
from cerno.core.chart import Chart, chart
from cerno.core.layer import Layer
from cerno.core.canvas import Canvas


# ── Chart construction ──────────────────────────────────────────────

class TestChartConstruction:
    def test_chart_factory_returns_chart(self):
        c = chart()
        assert isinstance(c, Chart)

    def test_cerno_chart_entry_point(self, sample_df):
        c = cerno.chart(sample_df)
        assert isinstance(c, Chart)
        assert c._data is sample_df

    def test_chart_no_data(self):
        c = chart()
        assert c._data is None

    def test_chart_initial_state(self):
        c = chart()
        assert c._layers == []
        assert c._title is None
        assert c._xlabel is None
        assert c._ylabel is None
        assert c._apply_funcs == []


# ── Method chaining ─────────────────────────────────────────────────

class TestChaining:
    def test_all_mark_methods_return_self(self, sample_df):
        c = cerno.chart(sample_df)
        assert c.scatter("x", "y") is c
        assert c.line("x", "y") is c
        assert c.bar("x", "y") is c
        assert c.histogram("x") is c

    def test_all_label_methods_return_self(self):
        c = chart()
        assert c.title("t") is c
        assert c.subtitle("s") is c
        assert c.xlabel("x") is c
        assert c.ylabel("y") is c
        assert c.caption("c") is c
        assert c.annotate("text", (1, 2)) is c

    def test_all_axis_methods_return_self(self):
        c = chart()
        assert c.xlim(0, 10) is c
        assert c.ylim(0, 10) is c
        assert c.xscale("log") is c
        assert c.yscale("log") is c
        assert c.xticks([1, 2, 3]) is c
        assert c.yticks([1, 2, 3]) is c

    def test_option_methods_return_self(self):
        c = chart()
        assert c.legend() is c
        assert c.theme("cerno_modern") is c
        assert c.size(10, 8) is c
        assert c.apply(lambda fig, ax: None) is c

    def test_output_methods_return_self(self, sample_df, tmp_path):
        c = cerno.chart(sample_df).scatter("x", "y")
        result = c.save(tmp_path / "test.png")
        assert result is c

    def test_full_chain(self, sample_df, tmp_path):
        """A realistic full chain should work without errors."""
        (
            cerno.chart(sample_df)
            .scatter("x", "y", color="cat", size="size_col")
            .title("Test Chart")
            .subtitle("A subtitle")
            .xlabel("X axis")
            .ylabel("Y axis")
            .caption("Source: test data")
            .xlim(0, 10)
            .ylim(0, 10)
            .legend(title="Categories")
            .save(tmp_path / "full_chain.png")
        )


# ── Layer registration ──────────────────────────────────────────────

class TestLayerRegistration:
    def test_scatter_adds_layer(self, sample_df):
        c = cerno.chart(sample_df).scatter("x", "y")
        assert len(c._layers) == 1
        assert c._layers[0].mark_type == "scatter"

    def test_line_adds_layer(self, sample_df):
        c = cerno.chart(sample_df).line("x", "y")
        assert len(c._layers) == 1
        assert c._layers[0].mark_type == "line"

    def test_bar_adds_layer(self, sample_df):
        c = cerno.chart(sample_df).bar("x", "y")
        assert len(c._layers) == 1
        assert c._layers[0].mark_type == "bar"

    def test_histogram_adds_layer(self, sample_df):
        c = cerno.chart(sample_df).histogram("x")
        assert len(c._layers) == 1
        assert c._layers[0].mark_type == "histogram"

    def test_multiple_layers(self, sample_df):
        c = cerno.chart(sample_df).scatter("x", "y").line("x", "y")
        assert len(c._layers) == 2

    def test_layer_stores_encodings(self, sample_df):
        c = cerno.chart(sample_df).scatter("x", "y", color="red", alpha=0.5)
        layer = c._layers[0]
        assert layer.encodings["color"] == "red"
        assert layer.encodings["alpha"] == 0.5

    def test_layer_stores_kwargs(self, sample_df):
        c = cerno.chart(sample_df).scatter("x", "y", marker="^")
        assert c._layers[0].kwargs["marker"] == "^"


# ── Decorators ──────────────────────────────────────────────────────

class TestDecorators:
    def test_title_stored(self):
        c = chart().title("My Title")
        assert c._title == "My Title"

    def test_subtitle_stored(self):
        c = chart().subtitle("Sub")
        assert c._subtitle == "Sub"

    def test_labels_stored(self):
        c = chart().xlabel("X").ylabel("Y")
        assert c._xlabel == "X"
        assert c._ylabel == "Y"

    def test_caption_stored(self):
        c = chart().caption("Source")
        assert c._caption == "Source"

    def test_limits_stored(self):
        c = chart().xlim(0, 10).ylim(-5, 5)
        assert c._xlim == (0, 10)
        assert c._ylim == (-5, 5)

    def test_scales_stored(self):
        c = chart().xscale("log").yscale("log")
        assert c._xscale == "log"
        assert c._yscale == "log"

    def test_ticks_stored(self):
        c = chart().xticks([1, 2], labels=["a", "b"], rotation=45)
        assert c._xticks["ticks"] == [1, 2]
        assert c._xticks["labels"] == ["a", "b"]
        assert c._xticks["rotation"] == 45

    def test_legend_stored(self):
        c = chart().legend(position="upper left", title="Legend", hide=False)
        assert c._legend_opts["position"] == "upper left"
        assert c._legend_opts["title"] == "Legend"

    def test_annotations_stored(self):
        c = chart().annotate("point", (1, 2)).annotate("other", (3, 4))
        assert len(c._annotations) == 2
        assert c._annotations[0] == {"text": "point", "xy": (1, 2)}


# ── Rendering ───────────────────────────────────────────────────────

class TestRendering:
    def test_render_returns_fig_and_axes(self, sample_df):
        import matplotlib.figure
        c = cerno.chart(sample_df).scatter("x", "y")
        fig, axes = c._render()
        assert isinstance(fig, matplotlib.figure.Figure)

    def test_title_applied_to_axes(self, sample_df):
        c = cerno.chart(sample_df).scatter("x", "y").title("Hello")
        _, axes = c._render()
        assert axes.get_title() == "Hello"

    def test_labels_applied(self, sample_df):
        c = cerno.chart(sample_df).scatter("x", "y").xlabel("X").ylabel("Y")
        _, axes = c._render()
        assert axes.get_xlabel() == "X"
        assert axes.get_ylabel() == "Y"

    def test_limits_applied(self, sample_df):
        c = cerno.chart(sample_df).scatter("x", "y").xlim(0, 100).ylim(-10, 10)
        _, axes = c._render()
        assert axes.get_xlim() == (0, 100)
        assert axes.get_ylim() == (-10, 10)

    def test_log_scale_applied(self, sample_df):
        c = cerno.chart(sample_df).scatter("x", "y").xscale("log")
        _, axes = c._render()
        assert axes.get_xscale() == "log"

    def test_apply_escape_hatch(self, sample_df):
        called = []
        def my_func(fig, axes):
            called.append(True)
            axes.axhline(y=3, color="red")

        c = cerno.chart(sample_df).scatter("x", "y").apply(my_func)
        c._render()
        assert called == [True]

    def test_multiple_apply_calls(self, sample_df):
        calls = []
        c = (
            cerno.chart(sample_df)
            .scatter("x", "y")
            .apply(lambda f, a: calls.append("first"))
            .apply(lambda f, a: calls.append("second"))
        )
        c._render()
        assert calls == ["first", "second"]


# ── Save ────────────────────────────────────────────────────────────

class TestSave:
    def test_save_creates_file(self, sample_df, tmp_path):
        path = tmp_path / "chart.png"
        cerno.chart(sample_df).scatter("x", "y").save(str(path))
        assert path.exists()
        assert path.stat().st_size > 0

    def test_save_pdf(self, sample_df, tmp_path):
        path = tmp_path / "chart.pdf"
        cerno.chart(sample_df).scatter("x", "y").save(str(path))
        assert path.exists()

    def test_save_custom_dpi(self, sample_df, tmp_path):
        path = tmp_path / "chart.png"
        cerno.chart(sample_df).scatter("x", "y").save(str(path), dpi=300)
        assert path.exists()


# ── Canvas ──────────────────────────────────────────────────────────

class TestCanvas:
    def test_lazy_build(self):
        c = Canvas()
        assert c._figure is None
        assert c._axes is None

    def test_build_creates_figure(self):
        c = Canvas()
        fig, axes = c.build()
        assert fig is not None
        assert axes is not None
        assert c._figure is not None

    def test_build_idempotent(self):
        c = Canvas()
        fig1, ax1 = c.build()
        fig2, ax2 = c.build()
        assert fig1 is fig2
        assert ax1 is ax2

    def test_custom_figsize(self):
        c = Canvas(figsize=(12, 6))
        fig, _ = c.build()
        w, h = fig.get_size_inches()
        assert w == pytest.approx(12)
        assert h == pytest.approx(6)

    def test_size_method_on_chart(self, sample_df):
        c = cerno.chart(sample_df).size(14, 7).scatter("x", "y")
        fig, _ = c._render()
        w, h = fig.get_size_inches()
        assert w == pytest.approx(14)
        assert h == pytest.approx(7)


# ── Layer dataclass ─────────────────────────────────────────────────

class TestLayer:
    def test_layer_defaults(self):
        layer = Layer(mark_type="scatter", x="x", y="y")
        assert layer.encodings == {}
        assert layer.kwargs == {}

    def test_layer_stores_fields(self):
        layer = Layer(
            mark_type="line", x="a", y="b",
            encodings={"color": "red"},
            kwargs={"linewidth": 2},
        )
        assert layer.mark_type == "line"
        assert layer.x == "a"
        assert layer.y == "b"
        assert layer.encodings["color"] == "red"
        assert layer.kwargs["linewidth"] == 2


# ── Input validation (Chart-level) ────────────────────────────────

class TestInputValidation:
    def test_scatter_alpha_out_of_range(self):
        with pytest.raises(ValueError, match="between 0 and 1"):
            chart().scatter("x", "y", alpha=2.0)

    def test_xlim_swapped(self):
        with pytest.raises(ValueError, match="Did you swap"):
            chart().xlim(10, 5)

    def test_ylim_swapped(self):
        with pytest.raises(ValueError, match="Did you swap"):
            chart().ylim(10, 5)

    def test_xscale_invalid(self):
        with pytest.raises(ValueError, match="unknown scale"):
            chart().xscale("logs")

    def test_xticks_labels_mismatch(self):
        with pytest.raises(ValueError, match="3 ticks but 2 labels"):
            chart().xticks(ticks=[1, 2, 3], labels=["a", "b"])

    def test_annotate_bad_xy(self):
        with pytest.raises(ValueError, match="length 3"):
            chart().annotate("hi", (1, 2, 3))

    def test_size_negative(self):
        with pytest.raises(ValueError, match="positive numbers"):
            chart().size(-1, 5)
