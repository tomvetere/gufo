"""Tests for gufo.marks — individual mark renderers."""
import numpy as np
import pandas as pd
import pytest
import matplotlib.pyplot as plt

import gufo
from gufo.data.adapter import DataAdapter
from gufo.marks._base import resolve_color, default_colors


# ── Shared utilities (_base.py) ─────────────────────────────────────

class TestResolveColor:
    def test_none_returns_none(self):
        adapter = DataAdapter(None)
        assert resolve_color(adapter, None) is None

    def test_literal_color_string(self):
        adapter = DataAdapter(None)
        assert resolve_color(adapter, "red") == "red"

    def test_column_name_resolves(self, sample_df):
        adapter = DataAdapter(sample_df)
        result = resolve_color(adapter, "cat")
        np.testing.assert_array_equal(result, ["a", "b", "a", "b", "a"])

    def test_non_string_passthrough(self):
        adapter = DataAdapter(None)
        color_tuple = (0.5, 0.5, 0.5)
        assert resolve_color(adapter, color_tuple) == color_tuple

    def test_missing_column_falls_back(self, sample_df):
        adapter = DataAdapter(sample_df)
        # "blue" is not a column name, so it falls back to literal
        assert resolve_color(adapter, "blue") == "blue"


class TestDefaultColors:
    def test_returns_correct_count(self):
        colors = default_colors(5)
        assert len(colors) == 5

    def test_wraps_around_at_palette_length(self):
        colors = default_colors(10)
        assert len(colors) == 10
        # GUFO_PALETTE has 8 colors, so index 8 wraps to index 0
        assert colors[0] == colors[8]

    def test_returns_hex_strings(self):
        colors = default_colors(3)
        assert all(isinstance(c, str) and c.startswith("#") for c in colors)


# ── Scatter ─────────────────────────────────────────────────────────

class TestScatterMark:
    def test_basic_scatter(self, sample_df, tmp_path):
        gufo.chart(sample_df).scatter("x", "y").save(tmp_path / "s.png")

    def test_scatter_with_literal_color(self, sample_df, tmp_path):
        gufo.chart(sample_df).scatter("x", "y", color="red").save(tmp_path / "s.png")

    def test_scatter_with_categorical_color(self, sample_df, tmp_path):
        gufo.chart(sample_df).scatter("x", "y", color="cat").save(tmp_path / "s.png")

    def test_scatter_categorical_creates_groups(self, sample_df):
        c = gufo.chart(sample_df).scatter("x", "y", color="cat")
        _, axes = c._render()
        # Categorical scatter creates one collection per category
        # "a" appears 3 times, "b" appears 2 times → 2 scatter calls
        collections = axes.collections
        assert len(collections) == 2

    def test_scatter_with_size_encoding(self, sample_df, tmp_path):
        gufo.chart(sample_df).scatter("x", "y", size="size_col").save(tmp_path / "s.png")

    def test_scatter_with_alpha(self, sample_df, tmp_path):
        gufo.chart(sample_df).scatter("x", "y", alpha=0.5).save(tmp_path / "s.png")

    def test_scatter_with_label(self, sample_df, tmp_path):
        gufo.chart(sample_df).scatter("x", "y", label="points").save(tmp_path / "s.png")

    def test_scatter_categorical_color_and_size(self, sample_df, tmp_path):
        (gufo.chart(sample_df)
         .scatter("x", "y", color="cat", size="size_col")
         .save(tmp_path / "s.png"))

    def test_scatter_with_arrays(self, tmp_path):
        gufo.chart().scatter([1, 2, 3], [4, 5, 6]).save(tmp_path / "s.png")

    def test_scatter_extra_kwargs(self, sample_df, tmp_path):
        gufo.chart(sample_df).scatter("x", "y", marker="^").save(tmp_path / "s.png")

    def test_scatter_wide_form(self, sample_df, tmp_path):
        gufo.chart(sample_df).scatter("x", ["series_a", "series_b"]).save(tmp_path / "s.png")

    def test_scatter_wide_form_creates_multiple_collections(self, sample_df):
        c = gufo.chart(sample_df).scatter("x", ["series_a", "series_b"])
        _, axes = c._render()
        assert len(axes.collections) == 2

    def test_scatter_wide_form_with_alpha(self, sample_df, tmp_path):
        gufo.chart(sample_df).scatter("x", ["series_a", "series_b"], alpha=0.5).save(tmp_path / "s.png")


# ── Scatter continuous color ───────────────────────────────────────

class TestScatterContinuousColor:
    @pytest.fixture
    def cont_df(self):
        return pd.DataFrame({
            "x": [1, 2, 3, 4, 5],
            "y": [2, 4, 1, 5, 3],
            "temp": [10.0, 20.0, 30.0, 40.0, 50.0],
            "cat": ["a", "b", "a", "b", "a"],
        })

    def test_scatter_continuous_color(self, cont_df, tmp_path):
        gufo.chart(cont_df).scatter("x", "y", color="temp").save(tmp_path / "s.png")

    def test_scatter_cmap(self, cont_df, tmp_path):
        gufo.chart(cont_df).scatter("x", "y", color="temp", cmap="coolwarm").save(tmp_path / "s.png")

    def test_scatter_vmin_vmax(self, cont_df, tmp_path):
        gufo.chart(cont_df).scatter("x", "y", color="temp", vmin=0, vmax=100).save(tmp_path / "s.png")

    def test_scatter_colorbar_present(self, cont_df):
        c = gufo.chart(cont_df).scatter("x", "y", color="temp")
        fig, axes = c._render()
        # Colorbar adds an extra axes to the figure
        assert len(fig.axes) == 2

    def test_scatter_colorbar_disabled(self, cont_df):
        c = gufo.chart(cont_df).scatter("x", "y", color="temp", colorbar=False)
        fig, axes = c._render()
        assert len(fig.axes) == 1

    def test_scatter_categorical_no_colorbar(self, cont_df):
        c = gufo.chart(cont_df).scatter("x", "y", color="cat")
        fig, axes = c._render()
        # Categorical color should not produce a colorbar
        assert len(fig.axes) == 1


# ── Line ────────────────────────────────────────────────────────────

class TestLineMark:
    def test_basic_line(self, sample_df, tmp_path):
        gufo.chart(sample_df).line("x", "y").save(tmp_path / "l.png")

    def test_line_with_literal_color(self, sample_df, tmp_path):
        gufo.chart(sample_df).line("x", "y", color="green").save(tmp_path / "l.png")

    def test_line_wide_form(self, sample_df, tmp_path):
        gufo.chart(sample_df).line("x", ["series_a", "series_b"]).save(tmp_path / "l.png")

    def test_line_wide_form_creates_multiple_lines(self, sample_df):
        c = gufo.chart(sample_df).line("x", ["series_a", "series_b"])
        _, axes = c._render()
        assert len(axes.get_lines()) == 2

    def test_line_categorical_color_grouping(self, sample_df):
        c = gufo.chart(sample_df).line("x", "y", color="cat")
        _, axes = c._render()
        # Two categories → two lines
        assert len(axes.get_lines()) == 2

    def test_line_stroke_dash(self, sample_df, tmp_path):
        gufo.chart(sample_df).line("x", "y", stroke_dash="dashed").save(tmp_path / "l.png")

    def test_line_with_arrays(self, tmp_path):
        gufo.chart().line([1, 2, 3], [4, 5, 6]).save(tmp_path / "l.png")


# ── Bar ─────────────────────────────────────────────────────────────

class TestBarMark:
    def test_basic_bar(self, sample_df, tmp_path):
        gufo.chart(sample_df).bar("x", "y").save(tmp_path / "b.png")

    def test_bar_horizontal(self, sample_df, tmp_path):
        gufo.chart(sample_df).bar("x", "y", horizontal=True).save(tmp_path / "b.png")

    def test_bar_with_color(self, sample_df, tmp_path):
        gufo.chart(sample_df).bar("x", "y", color="orange").save(tmp_path / "b.png")

    def test_bar_with_arrays(self, tmp_path):
        data = {"cat": ["a", "b", "c"], "val": [1, 2, 3]}
        gufo.chart(data).bar("cat", "val").save(tmp_path / "b.png")

    def test_bar_wide_form(self, sample_df, tmp_path):
        gufo.chart(sample_df).bar("x", ["series_a", "series_b"]).save(tmp_path / "b.png")

    def test_bar_wide_form_grouped(self, sample_df):
        c = gufo.chart(sample_df).bar("x", ["series_a", "series_b"])
        _, axes = c._render()
        # 2 series × 5 x-values = 10 patches
        assert len(axes.patches) == 10

    def test_bar_wide_form_horizontal(self, sample_df, tmp_path):
        gufo.chart(sample_df).bar("x", ["series_a", "series_b"], horizontal=True).save(tmp_path / "b.png")


# ── Bar grouped/stacked ───────────────────────────────────────────

class TestBarGrouped:
    @pytest.fixture
    def grouped_df(self):
        return pd.DataFrame({
            "quarter": ["Q1", "Q2", "Q1", "Q2"],
            "revenue": [100, 150, 200, 250],
            "region": ["East", "East", "West", "West"],
        })

    def test_bar_dodged_by_color(self, grouped_df):
        c = gufo.chart(grouped_df).bar("quarter", "revenue", color="region")
        _, axes = c._render()
        # 2 quarters × 2 regions = 4 patches
        assert len(axes.patches) == 4

    def test_bar_stacked_by_color(self, grouped_df):
        c = gufo.chart(grouped_df).bar("quarter", "revenue", color="region", stacked=True)
        _, axes = c._render()
        # 2 quarters × 2 regions = 4 patches
        assert len(axes.patches) == 4

    def test_bar_dodged_horizontal(self, grouped_df, tmp_path):
        gufo.chart(grouped_df).bar("quarter", "revenue", color="region", horizontal=True).save(tmp_path / "b.png")

    def test_bar_stacked_horizontal(self, grouped_df, tmp_path):
        gufo.chart(grouped_df).bar("quarter", "revenue", color="region", stacked=True, horizontal=True).save(tmp_path / "b.png")

    def test_bar_dodged_with_dict_data(self, tmp_path):
        data = {
            "quarter": ["Q1", "Q2", "Q1", "Q2"],
            "revenue": [100, 150, 200, 250],
            "region": ["East", "East", "West", "West"],
        }
        gufo.chart(data).bar("quarter", "revenue", color="region").save(tmp_path / "b.png")

    def test_bar_stacked_values_correct(self, grouped_df):
        c = gufo.chart(grouped_df).bar("quarter", "revenue", color="region", stacked=True)
        _, axes = c._render()
        # Stacked bars: Q1 = 100 + 200 = 300, Q2 = 150 + 250 = 400
        # The top of the stack should equal the total
        heights = [p.get_height() for p in axes.patches]
        # First 2 patches are East (100, 150), next 2 are West (200, 250)
        assert heights == [100.0, 150.0, 200.0, 250.0]

    def test_bar_dodged_legend_labels(self, grouped_df):
        c = gufo.chart(grouped_df).bar("quarter", "revenue", color="region").legend()
        _, axes = c._render()
        legend = axes.get_legend()
        labels = [t.get_text() for t in legend.get_texts()]
        assert "East" in labels
        assert "West" in labels


# ── Histogram ───────────────────────────────────────────────────────

class TestHistogramMark:
    def test_basic_histogram(self, sample_df, tmp_path):
        gufo.chart(sample_df).histogram("x").save(tmp_path / "h.png")

    def test_histogram_custom_bins(self, sample_df, tmp_path):
        gufo.chart(sample_df).histogram("x", bins=10).save(tmp_path / "h.png")

    def test_histogram_with_color(self, sample_df, tmp_path):
        gufo.chart(sample_df).histogram("x", color="purple").save(tmp_path / "h.png")

    def test_histogram_with_arrays(self, tmp_path):
        gufo.chart().histogram([1, 1, 2, 3, 3, 3, 4]).save(tmp_path / "h.png")

    def test_histogram_density(self, sample_df, tmp_path):
        gufo.chart(sample_df).histogram("x", density=True).save(tmp_path / "h.png")

    def test_histogram_extra_kwargs(self, sample_df, tmp_path):
        gufo.chart(sample_df).histogram("x", histtype="step").save(tmp_path / "h.png")


# ── Multi-layer ─────────────────────────────────────────────────────

class TestMultiLayer:
    def test_scatter_plus_line(self, sample_df, tmp_path):
        (gufo.chart(sample_df)
         .scatter("x", "y")
         .line("x", "series_a")
         .save(tmp_path / "multi.png"))

    def test_layers_render_in_order(self, sample_df):
        c = gufo.chart(sample_df).scatter("x", "y").line("x", "y")
        assert c._layers[0].mark_type == "scatter"
        assert c._layers[1].mark_type == "line"


class TestChartClear:
    def test_clear_removes_layers(self, sample_df):
        c = gufo.chart(sample_df).scatter("x", "y").line("x", "y")
        assert len(c._layers) == 2
        c.clear()
        assert c._layers == []

    def test_clear_returns_self(self, sample_df):
        c = gufo.chart(sample_df).scatter("x", "y")
        assert c.clear() is c

    def test_clear_chainable(self, sample_df, tmp_path):
        c = gufo.chart(sample_df).histogram("x")
        (c.clear()
         .histogram("x", density=True)
         .save(tmp_path / "cleared.png"))
        assert len(c._layers) == 1
        assert c._layers[0].encodings.get("density") is True

    def test_clear_preserves_data_and_theme(self, sample_df):
        c = (gufo.chart(sample_df)
             .theme("gufo_dark")
             .palette(["#ff0000", "#00ff00"])
             .size(10, 6)
             .scatter("x", "y"))
        c.clear()
        assert c._data is sample_df
        assert c._theme_override == "gufo_dark"
        assert c._palette == ["#ff0000", "#00ff00"]
        assert c._canvas._figsize == (10, 6)

    def test_clear_resets_decorators(self, sample_df):
        c = (gufo.chart(sample_df)
             .scatter("x", "y")
             .title("before")
             .xlabel("X")
             .ylabel("Y")
             .xlim(0, 10)
             .annotate("note", (1, 2))
             .hline(0)
             .legend()
             .label())
        c.clear()
        assert c._title is None
        assert c._xlabel is None
        assert c._ylabel is None
        assert c._xlim is None
        assert c._annotations == []
        assert c._references == []
        assert c._legend_opts is None
        assert c._label_config is None

    def test_clear_then_render_shows_only_new_layers(self, sample_df, tmp_path):
        c = gufo.chart(sample_df).scatter("x", "y")
        c.save(tmp_path / "first.png")
        c.clear().line("x", "y")
        c.save(tmp_path / "second.png")
        assert len(c._layers) == 1
        assert c._layers[0].mark_type == "line"


# ── Mark-level validation ─────────────────────────────────────────

class TestMarkValidation:
    def test_scatter_length_mismatch(self, tmp_path):
        c = gufo.chart().scatter(np.arange(5), np.arange(3))
        with pytest.raises(ValueError, match="array length mismatch"):
            c.save(tmp_path / "bad.png")

    def test_bar_length_mismatch(self, tmp_path):
        c = gufo.chart().bar(np.arange(5), np.arange(3))
        with pytest.raises(ValueError, match="array length mismatch"):
            c.save(tmp_path / "bad.png")

    def test_histogram_non_numeric(self, tmp_path):
        c = gufo.chart().histogram(np.array(["a", "b", "c"]))
        with pytest.raises(ValueError, match="must be numeric"):
            c.save(tmp_path / "bad.png")

    def test_scatter_nan_warns(self, tmp_path):
        x = np.array([1.0, 2.0, np.nan])
        y = np.array([1.0, 2.0, 3.0])
        c = gufo.chart().scatter(x, y)
        with pytest.warns(UserWarning, match="NaN"):
            c.save(tmp_path / "nan.png")

    def test_line_length_mismatch(self, tmp_path):
        c = gufo.chart().line(np.arange(5), np.arange(3))
        with pytest.raises(ValueError, match="array length mismatch"):
            c.save(tmp_path / "bad.png")


# ── Box plot ───────────────────────────────────────────────────────

class TestBoxplotMark:
    def test_basic_boxplot(self, sample_df, tmp_path):
        gufo.chart(sample_df).boxplot("cat", "y").save(tmp_path / "bp.png")

    def test_boxplot_horizontal(self, sample_df, tmp_path):
        gufo.chart(sample_df).boxplot("cat", "y", horizontal=True).save(tmp_path / "bp.png")

    def test_boxplot_with_color(self, sample_df, tmp_path):
        gufo.chart(sample_df).boxplot("cat", "y", color="steelblue").save(tmp_path / "bp.png")

    def test_boxplot_wide_form(self, sample_df, tmp_path):
        gufo.chart(sample_df).boxplot("x", ["series_a", "series_b"]).save(tmp_path / "bp.png")

    def test_boxplot_wide_form_box_count(self, sample_df):
        c = gufo.chart(sample_df).boxplot("x", ["series_a", "series_b"])
        _, axes = c._render()
        # patch_artist=True creates one patch per box
        assert len(axes.patches) == 2

    def test_boxplot_with_dict_data(self, tmp_path):
        data = {"g": ["a", "a", "b", "b"], "v": [1, 2, 3, 4]}
        gufo.chart(data).boxplot("g", "v").save(tmp_path / "bp.png")

    def test_boxplot_nan_warns(self, tmp_path):
        data = {"g": ["a", "a", "b", "b"], "v": [1.0, np.nan, 3.0, 4.0]}
        c = gufo.chart(data).boxplot("g", "v")
        with pytest.warns(UserWarning, match="NaN"):
            c.save(tmp_path / "bp.png")

    def test_boxplot_extra_kwargs(self, sample_df, tmp_path):
        gufo.chart(sample_df).boxplot("cat", "y", whis=1.5).save(tmp_path / "bp.png")


# ── Violin ─────────────────────────────────────────────────────────

class TestViolinMark:
    def test_basic_violin(self, sample_df, tmp_path):
        gufo.chart(sample_df).violin("cat", "y").save(tmp_path / "v.png")

    def test_violin_horizontal(self, sample_df, tmp_path):
        gufo.chart(sample_df).violin("cat", "y", horizontal=True).save(tmp_path / "v.png")

    def test_violin_with_color(self, sample_df, tmp_path):
        gufo.chart(sample_df).violin("cat", "y", color="steelblue").save(tmp_path / "v.png")

    def test_violin_wide_form(self, sample_df, tmp_path):
        gufo.chart(sample_df).violin("x", ["series_a", "series_b"]).save(tmp_path / "v.png")

    def test_violin_wide_form_body_count(self, sample_df):
        chart = gufo.chart(sample_df).violin("x", ["series_a", "series_b"])
        _, axes = chart._render()
        # Each wide-form column produces one PolyCollection body
        polys = [col for col in axes.collections if hasattr(col, "get_facecolor")]
        assert len(polys) >= 2

    def test_violin_with_dict_data(self, tmp_path):
        data = {"g": ["a", "a", "b", "b"], "v": [1, 2, 3, 4]}
        gufo.chart(data).violin("g", "v").save(tmp_path / "v.png")

    def test_violin_nan_warns(self, tmp_path):
        data = {"g": ["a", "a", "b", "b"], "v": [1.0, np.nan, 3.0, 4.0]}
        c = gufo.chart(data).violin("g", "v")
        with pytest.warns(UserWarning, match="NaN"):
            c.save(tmp_path / "v.png")

    def test_violin_extra_kwargs(self, sample_df, tmp_path):
        gufo.chart(sample_df).violin("cat", "y", showmeans=True).save(tmp_path / "v.png")


# ── Heatmap ────────────────────────────────────────────────────────

class TestHeatmapMark:
    def test_heatmap_matrix_form(self, tmp_path):
        matrix_df = pd.DataFrame(
            [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
            index=["a", "b", "c"],
            columns=["x", "y", "z"],
        )
        gufo.chart(matrix_df).heatmap().save(tmp_path / "hm.png")

    def test_heatmap_long_form(self, tmp_path):
        df = pd.DataFrame({
            "row": ["a", "a", "b", "b"],
            "col": ["x", "y", "x", "y"],
            "val": [1, 2, 3, 4],
        })
        gufo.chart(df).heatmap("col", "row", color="val").save(tmp_path / "hm.png")

    def test_heatmap_with_cmap(self, tmp_path):
        matrix_df = pd.DataFrame([[1, 2], [3, 4]])
        gufo.chart(matrix_df).heatmap(cmap="coolwarm").save(tmp_path / "hm.png")

    def test_heatmap_annotated(self, tmp_path):
        matrix_df = pd.DataFrame([[1, 2], [3, 4]])
        gufo.chart(matrix_df).heatmap(annotate=True).save(tmp_path / "hm.png")

    def test_heatmap_long_form_missing_color_raises(self, tmp_path):
        df = pd.DataFrame({"a": [1, 2], "b": [3, 4]})
        c = gufo.chart(df).heatmap("a", "b")
        with pytest.raises(ValueError, match="color encoding"):
            c.save(tmp_path / "hm.png")

    def test_heatmap_dict_matrix_raises(self, tmp_path):
        c = gufo.chart({"a": [1, 2]}).heatmap()
        with pytest.raises(ValueError, match="DataFrame"):
            c.save(tmp_path / "hm.png")


# ── Area ───────────────────────────────────────────────────────────

class TestAreaMark:
    def test_basic_area(self, sample_df, tmp_path):
        gufo.chart(sample_df).area("x", "y").save(tmp_path / "a.png")

    def test_area_with_color(self, sample_df, tmp_path):
        gufo.chart(sample_df).area("x", "y", color="steelblue").save(tmp_path / "a.png")

    def test_area_with_alpha(self, sample_df, tmp_path):
        gufo.chart(sample_df).area("x", "y", alpha=0.3).save(tmp_path / "a.png")

    def test_area_wide_form(self, sample_df, tmp_path):
        gufo.chart(sample_df).area("x", ["series_a", "series_b"]).save(tmp_path / "a.png")

    def test_area_categorical_color(self, sample_df, tmp_path):
        gufo.chart(sample_df).area("x", "y", color="cat").save(tmp_path / "a.png")

    def test_area_with_arrays(self, tmp_path):
        gufo.chart().area([1, 2, 3], [4, 5, 6]).save(tmp_path / "a.png")

    def test_area_length_mismatch(self, tmp_path):
        c = gufo.chart().area(np.arange(5), np.arange(3))
        with pytest.raises(ValueError, match="array length mismatch"):
            c.save(tmp_path / "a.png")

    def test_area_nan_warns(self, tmp_path):
        x = np.array([1.0, 2.0, 3.0])
        y = np.array([1.0, np.nan, 3.0])
        c = gufo.chart().area(x, y)
        with pytest.warns(UserWarning, match="NaN"):
            c.save(tmp_path / "a.png")


# ── Boxplot categorical color ─────────────────────────────────────

class TestBoxplotCategoricalColor:
    def test_boxplot_grouped_by_color(self, tmp_path):
        df = pd.DataFrame({
            "group": ["A", "A", "A", "B", "B", "B"] * 2,
            "value": [1, 2, 3, 4, 5, 6, 2, 3, 4, 5, 6, 7],
            "hue": ["x", "x", "x", "x", "x", "x", "y", "y", "y", "y", "y", "y"],
        })
        (gufo.chart(df)
         .boxplot("group", "value", color="hue")
         .save(tmp_path / "b.png"))

    def test_boxplot_grouped_horizontal(self, tmp_path):
        df = pd.DataFrame({
            "group": ["A", "A", "B", "B"],
            "value": [1, 2, 3, 4],
            "hue": ["x", "y", "x", "y"],
        })
        (gufo.chart(df)
         .boxplot("group", "value", color="hue", horizontal=True)
         .save(tmp_path / "b.png"))


# ── Violin categorical color ──────────────────────────────────────

class TestViolinCategoricalColor:
    def test_violin_grouped_by_color(self, tmp_path):
        rng = np.random.default_rng(0)
        df = pd.DataFrame({
            "group": ["A"] * 20 + ["B"] * 20,
            "value": rng.normal(size=40),
            "hue": (["x"] * 10 + ["y"] * 10) * 2,
        })
        (gufo.chart(df)
         .violin("group", "value", color="hue")
         .save(tmp_path / "v.png"))


# ── Countplot ─────────────────────────────────────────────────────

class TestCountplot:
    def test_basic_countplot(self, sample_df, tmp_path):
        gufo.chart(sample_df).countplot("cat").save(tmp_path / "c.png")

    def test_countplot_horizontal(self, sample_df, tmp_path):
        gufo.chart(sample_df).countplot("cat", horizontal=True).save(tmp_path / "c.png")

    def test_countplot_with_literal_color(self, sample_df, tmp_path):
        gufo.chart(sample_df).countplot("cat", color="coral").save(tmp_path / "c.png")

    def test_countplot_grouped(self, tmp_path):
        df = pd.DataFrame({
            "animal": ["cat", "dog", "cat", "dog", "cat", "dog"],
            "color": ["black", "black", "white", "white", "black", "white"],
        })
        (gufo.chart(df)
         .countplot("animal", color="color")
         .save(tmp_path / "c.png"))


# ── ECDF ──────────────────────────────────────────────────────────

class TestEcdf:
    def test_basic_ecdf(self, sample_df, tmp_path):
        gufo.chart(sample_df).ecdf("y").save(tmp_path / "e.png")

    def test_ecdf_with_color(self, sample_df, tmp_path):
        gufo.chart(sample_df).ecdf("y", color="steelblue").save(tmp_path / "e.png")

    def test_ecdf_categorical_color(self, sample_df, tmp_path):
        gufo.chart(sample_df).ecdf("y", color="cat").save(tmp_path / "e.png")

    def test_ecdf_with_nan(self, tmp_path):
        data = {"v": [1.0, 2.0, np.nan, 4.0]}
        c = gufo.chart(data).ecdf("v")
        with pytest.warns(UserWarning, match="NaN"):
            c.save(tmp_path / "e.png")

    def test_ecdf_with_label(self, sample_df, tmp_path):
        (gufo.chart(sample_df)
         .ecdf("y", label="values")
         .legend()
         .save(tmp_path / "e.png"))


# ── Rugplot ───────────────────────────────────────────────────────

class TestRug:
    def test_basic_rug(self, sample_df, tmp_path):
        gufo.chart(sample_df).rug("x").save(tmp_path / "r.png")

    def test_rug_with_color(self, sample_df, tmp_path):
        gufo.chart(sample_df).rug("x", color="red").save(tmp_path / "r.png")

    def test_rug_categorical_color(self, sample_df, tmp_path):
        gufo.chart(sample_df).rug("x", color="cat").save(tmp_path / "r.png")

    def test_rug_custom_height_alpha(self, sample_df, tmp_path):
        gufo.chart(sample_df).rug("x", height=0.1, alpha=0.8).save(tmp_path / "r.png")

    def test_rug_layered_with_histogram(self, sample_df, tmp_path):
        (gufo.chart(sample_df)
         .histogram("y")
         .rug("y")
         .save(tmp_path / "r.png"))


# ── Error bars ────────────────────────────────────────────────────

class TestErrorBars:
    def test_scatter_yerr(self, tmp_path):
        (gufo.chart()
         .scatter([1, 2, 3], [4, 5, 6], y_error=[0.5, 0.3, 0.4])
         .save(tmp_path / "e.png"))

    def test_scatter_xerr(self, tmp_path):
        (gufo.chart()
         .scatter([1, 2, 3], [4, 5, 6], x_error=[0.1, 0.2, 0.1])
         .save(tmp_path / "e.png"))

    def test_scatter_both_errors(self, tmp_path):
        (gufo.chart()
         .scatter([1, 2, 3], [4, 5, 6], y_error=[0.5, 0.3, 0.4],
                  x_error=[0.1, 0.2, 0.1])
         .save(tmp_path / "e.png"))

    def test_line_yerr(self, tmp_path):
        (gufo.chart()
         .line([1, 2, 3], [4, 5, 6], y_error=[0.5, 0.3, 0.4])
         .save(tmp_path / "e.png"))

    def test_bar_yerr(self, tmp_path):
        df = pd.DataFrame({"x": ["a", "b", "c"], "y": [4, 5, 6],
                           "err": [0.5, 0.3, 0.4]})
        (gufo.chart(df)
         .bar("x", "y", y_error="err")
         .save(tmp_path / "e.png"))

    def test_bar_yerr_from_column(self, tmp_path):
        df = pd.DataFrame({
            "x": ["a", "b", "c"],
            "y": [4, 5, 6],
            "err": [0.5, 0.3, 0.4],
        })
        (gufo.chart(df)
         .bar("x", "y", y_error="err")
         .save(tmp_path / "e.png"))


# ── Pointplot ─────────────────────────────────────────────────────

class TestPointplot:
    @pytest.fixture
    def point_df(self):
        return pd.DataFrame({
            "day": ["Mon", "Mon", "Mon", "Tue", "Tue", "Tue",
                    "Wed", "Wed", "Wed"],
            "tip": [3.0, 4.0, 5.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0],
            "sex": ["M", "F", "M", "F", "M", "F", "M", "F", "M"],
        })

    def test_basic(self, point_df, tmp_path):
        (gufo.chart(point_df)
         .pointplot("day", "tip")
         .save(tmp_path / "p.png"))
        assert (tmp_path / "p.png").exists()

    def test_grouped(self, point_df, tmp_path):
        (gufo.chart(point_df)
         .pointplot("day", "tip", color="sex")
         .save(tmp_path / "p.png"))

    def test_horizontal(self, point_df, tmp_path):
        (gufo.chart(point_df)
         .pointplot("day", "tip", horizontal=True)
         .save(tmp_path / "p.png"))

    def test_renders_errorbars(self, point_df):
        c = gufo.chart(point_df).pointplot("day", "tip")
        _, axes = c._render()
        # errorbar creates Line2D objects (means + error lines)
        assert len(axes.lines) > 0

    def test_has_three_tick_labels(self, point_df):
        c = gufo.chart(point_df).pointplot("day", "tip")
        _, axes = c._render()
        labels = [t.get_text() for t in axes.get_xticklabels()]
        assert "Mon" in labels
        assert "Tue" in labels
        assert "Wed" in labels

    def test_chaining(self, point_df):
        from gufo.core.chart import Chart
        c = gufo.chart(point_df).pointplot("day", "tip").title("Points")
        assert isinstance(c, Chart)


# ── v0.0.8: continuous color on line ───────────────────────────────

class TestLineContinuousColor:
    @pytest.fixture
    def line_df(self):
        return pd.DataFrame({
            "x": np.linspace(0, 10, 20),
            "y": np.sin(np.linspace(0, 10, 20)),
            "z": np.linspace(0, 1, 20),
        })

    def test_renders_as_line_collection(self, line_df):
        c = gufo.chart(line_df).line("x", "y", color="z", cmap="viridis")
        fig, ax = c._render()
        # Continuous-color line uses LineCollection, not plain Line2D
        assert len(ax.collections) == 1
        from matplotlib.collections import LineCollection
        assert isinstance(ax.collections[0], LineCollection)
        plt.close(fig)

    def test_colorbar_drawn_by_default(self, line_df):
        c = gufo.chart(line_df).line("x", "y", color="z", cmap="viridis")
        fig, ax = c._render()
        # fig.axes includes the main axes plus the colorbar axes
        assert len(fig.axes) == 2
        plt.close(fig)

    def test_colorbar_false_hides_colorbar(self, line_df):
        c = gufo.chart(line_df).line(
            "x", "y", color="z", cmap="viridis", colorbar=False
        )
        fig, ax = c._render()
        assert len(fig.axes) == 1
        plt.close(fig)

    def test_vmin_vmax_respected(self, line_df):
        c = gufo.chart(line_df).line(
            "x", "y", color="z", cmap="viridis", vmin=-1, vmax=2
        )
        fig, ax = c._render()
        lc = ax.collections[0]
        assert lc.norm.vmin == -1
        assert lc.norm.vmax == 2
        plt.close(fig)

    def test_categorical_color_still_grouped(self, line_df):
        df = line_df.copy()
        df["kind"] = ["a"] * 10 + ["b"] * 10
        c = gufo.chart(df).line("x", "y", color="kind")
        fig, ax = c._render()
        # Categorical should use the existing per-group Line2D path
        assert len(ax.lines) == 2
        assert len(ax.collections) == 0
        plt.close(fig)


# ── v0.0.8: .label() on line and pointplot ─────────────────────────

class TestLabelOnLine:
    @pytest.fixture
    def line_df(self):
        return pd.DataFrame({
            "x": [1, 2, 3, 4],
            "y": [10.0, 25.0, 13.0, 40.0],
            "name": ["A", "B", "C", "D"],
        })

    def test_label_line_with_column(self, line_df):
        c = gufo.chart(line_df).line("x", "y").label("name")
        fig, ax = c._render()
        texts = [t.get_text() for t in ax.texts]
        assert texts == ["A", "B", "C", "D"]
        plt.close(fig)

    def test_label_line_without_column_uses_y(self, line_df):
        c = gufo.chart(line_df).line("x", "y").label(fmt=".1f")
        fig, ax = c._render()
        texts = [t.get_text() for t in ax.texts]
        assert texts == ["10.0", "25.0", "13.0", "40.0"]
        plt.close(fig)

    def test_line_label_does_not_touch_references(self, line_df):
        c = (gufo.chart(line_df)
             .line("x", "y")
             .label("name")
             .hline(20))
        fig, ax = c._render()
        texts = [t.get_text() for t in ax.texts]
        assert texts == ["A", "B", "C", "D"]
        plt.close(fig)

    def test_label_pointplot_uses_means(self):
        df = pd.DataFrame({
            "cat": ["a", "a", "b", "b", "c", "c"],
            "val": [1.0, 3.0, 5.0, 7.0, 9.0, 11.0],
        })
        c = gufo.chart(df).pointplot("cat", "val").label(fmt=".1f")
        fig, ax = c._render()
        texts = [t.get_text() for t in ax.texts]
        # Means: a=2, b=6, c=10
        assert texts == ["2.0", "6.0", "10.0"]
        plt.close(fig)


# ── v0.0.8: area error bands ───────────────────────────────────────

class TestAreaErrorBand:
    @pytest.fixture
    def area_df(self):
        return pd.DataFrame({
            "x": list(range(6)),
            "y": [1.0, 2.0, 3.0, 4.0, 5.0, 6.0],
            "err": [0.5] * 6,
        })

    def test_error_band_adds_second_collection(self, area_df):
        c = gufo.chart(area_df).area("x", "y", y_error="err")
        fig, ax = c._render()
        # fill_between adds PolyCollection; base area + error band = 2
        assert len(ax.collections) == 2
        plt.close(fig)

    def test_no_error_band_without_param(self, area_df):
        c = gufo.chart(area_df).area("x", "y")
        fig, ax = c._render()
        assert len(ax.collections) == 1
        plt.close(fig)

    def test_error_array_accepted(self, area_df):
        err = np.full(6, 0.25)
        c = gufo.chart(area_df).area("x", "y", y_error=err)
        fig, ax = c._render()
        assert len(ax.collections) == 2
        plt.close(fig)

    def test_error_band_within_bounds(self, area_df):
        c = gufo.chart(area_df).area("x", "y", y_error="err")
        fig, ax = c._render()
        band = ax.collections[1]
        ys = band.get_paths()[0].vertices[:, 1]
        # Error band spans y ± 0.5 → overall y range [0.5, 6.5]
        assert ys.min() >= 0.4 and ys.max() <= 6.6
        plt.close(fig)
