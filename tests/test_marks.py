"""Tests for cerno.marks — individual mark renderers."""
import numpy as np
import pandas as pd
import pytest
import matplotlib.pyplot as plt

import cerno
from cerno.data.adapter import DataAdapter
from cerno.marks._base import resolve_color, default_colors


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
        # CERNO_PALETTE has 8 colors, so index 8 wraps to index 0
        assert colors[0] == colors[8]

    def test_returns_hex_strings(self):
        colors = default_colors(3)
        assert all(isinstance(c, str) and c.startswith("#") for c in colors)


# ── Scatter ─────────────────────────────────────────────────────────

class TestScatterMark:
    def test_basic_scatter(self, sample_df, tmp_path):
        cerno.chart(sample_df).scatter("x", "y").save(tmp_path / "s.png")

    def test_scatter_with_literal_color(self, sample_df, tmp_path):
        cerno.chart(sample_df).scatter("x", "y", color="red").save(tmp_path / "s.png")

    def test_scatter_with_categorical_color(self, sample_df, tmp_path):
        cerno.chart(sample_df).scatter("x", "y", color="cat").save(tmp_path / "s.png")

    def test_scatter_categorical_creates_groups(self, sample_df):
        c = cerno.chart(sample_df).scatter("x", "y", color="cat")
        _, axes = c._render()
        # Categorical scatter creates one collection per category
        # "a" appears 3 times, "b" appears 2 times → 2 scatter calls
        collections = axes.collections
        assert len(collections) == 2

    def test_scatter_with_size_encoding(self, sample_df, tmp_path):
        cerno.chart(sample_df).scatter("x", "y", size="size_col").save(tmp_path / "s.png")

    def test_scatter_with_alpha(self, sample_df, tmp_path):
        cerno.chart(sample_df).scatter("x", "y", alpha=0.5).save(tmp_path / "s.png")

    def test_scatter_with_label(self, sample_df, tmp_path):
        cerno.chart(sample_df).scatter("x", "y", label="points").save(tmp_path / "s.png")

    def test_scatter_categorical_color_and_size(self, sample_df, tmp_path):
        (cerno.chart(sample_df)
         .scatter("x", "y", color="cat", size="size_col")
         .save(tmp_path / "s.png"))

    def test_scatter_with_arrays(self, tmp_path):
        cerno.chart().scatter([1, 2, 3], [4, 5, 6]).save(tmp_path / "s.png")

    def test_scatter_extra_kwargs(self, sample_df, tmp_path):
        cerno.chart(sample_df).scatter("x", "y", marker="^").save(tmp_path / "s.png")


# ── Line ────────────────────────────────────────────────────────────

class TestLineMark:
    def test_basic_line(self, sample_df, tmp_path):
        cerno.chart(sample_df).line("x", "y").save(tmp_path / "l.png")

    def test_line_with_literal_color(self, sample_df, tmp_path):
        cerno.chart(sample_df).line("x", "y", color="green").save(tmp_path / "l.png")

    def test_line_wide_form(self, sample_df, tmp_path):
        cerno.chart(sample_df).line("x", ["series_a", "series_b"]).save(tmp_path / "l.png")

    def test_line_wide_form_creates_multiple_lines(self, sample_df):
        c = cerno.chart(sample_df).line("x", ["series_a", "series_b"])
        _, axes = c._render()
        assert len(axes.get_lines()) == 2

    def test_line_categorical_color_grouping(self, sample_df):
        c = cerno.chart(sample_df).line("x", "y", color="cat")
        _, axes = c._render()
        # Two categories → two lines
        assert len(axes.get_lines()) == 2

    def test_line_stroke_dash(self, sample_df, tmp_path):
        cerno.chart(sample_df).line("x", "y", stroke_dash="dashed").save(tmp_path / "l.png")

    def test_line_with_arrays(self, tmp_path):
        cerno.chart().line([1, 2, 3], [4, 5, 6]).save(tmp_path / "l.png")


# ── Bar ─────────────────────────────────────────────────────────────

class TestBarMark:
    def test_basic_bar(self, sample_df, tmp_path):
        cerno.chart(sample_df).bar("x", "y").save(tmp_path / "b.png")

    def test_bar_horizontal(self, sample_df, tmp_path):
        cerno.chart(sample_df).bar("x", "y", horizontal=True).save(tmp_path / "b.png")

    def test_bar_with_color(self, sample_df, tmp_path):
        cerno.chart(sample_df).bar("x", "y", color="orange").save(tmp_path / "b.png")

    def test_bar_with_arrays(self, tmp_path):
        data = {"cat": ["a", "b", "c"], "val": [1, 2, 3]}
        cerno.chart(data).bar("cat", "val").save(tmp_path / "b.png")


# ── Histogram ───────────────────────────────────────────────────────

class TestHistogramMark:
    def test_basic_histogram(self, sample_df, tmp_path):
        cerno.chart(sample_df).histogram("x").save(tmp_path / "h.png")

    def test_histogram_custom_bins(self, sample_df, tmp_path):
        cerno.chart(sample_df).histogram("x", bins=10).save(tmp_path / "h.png")

    def test_histogram_with_color(self, sample_df, tmp_path):
        cerno.chart(sample_df).histogram("x", color="purple").save(tmp_path / "h.png")

    def test_histogram_with_arrays(self, tmp_path):
        cerno.chart().histogram([1, 1, 2, 3, 3, 3, 4]).save(tmp_path / "h.png")


# ── Multi-layer ─────────────────────────────────────────────────────

class TestMultiLayer:
    def test_scatter_plus_line(self, sample_df, tmp_path):
        (cerno.chart(sample_df)
         .scatter("x", "y")
         .line("x", "series_a")
         .save(tmp_path / "multi.png"))

    def test_layers_render_in_order(self, sample_df):
        c = cerno.chart(sample_df).scatter("x", "y").line("x", "y")
        assert c._layers[0].mark_type == "scatter"
        assert c._layers[1].mark_type == "line"


# ── Mark-level validation ─────────────────────────────────────────

class TestMarkValidation:
    def test_scatter_length_mismatch(self, tmp_path):
        c = cerno.chart().scatter(np.arange(5), np.arange(3))
        with pytest.raises(ValueError, match="array length mismatch"):
            c.save(tmp_path / "bad.png")

    def test_bar_length_mismatch(self, tmp_path):
        c = cerno.chart().bar(np.arange(5), np.arange(3))
        with pytest.raises(ValueError, match="array length mismatch"):
            c.save(tmp_path / "bad.png")

    def test_histogram_non_numeric(self, tmp_path):
        c = cerno.chart().histogram(np.array(["a", "b", "c"]))
        with pytest.raises(ValueError, match="must be numeric"):
            c.save(tmp_path / "bad.png")

    def test_scatter_nan_warns(self, tmp_path):
        x = np.array([1.0, 2.0, np.nan])
        y = np.array([1.0, 2.0, 3.0])
        c = cerno.chart().scatter(x, y)
        with pytest.warns(UserWarning, match="NaN"):
            c.save(tmp_path / "nan.png")

    def test_line_length_mismatch(self, tmp_path):
        c = cerno.chart().line(np.arange(5), np.arange(3))
        with pytest.raises(ValueError, match="array length mismatch"):
            c.save(tmp_path / "bad.png")
