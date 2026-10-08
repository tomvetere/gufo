"""Tests for gufo.core.validate — input validation helpers."""
import warnings

import numpy as np
import pytest

import gufo
from gufo.core.validate import (
    check_array_lengths,
    check_numeric,
    check_stroke_dash,
    warn_nan_inf,
)


# ── check_array_lengths ──────────────────────────────────────────────

class TestCheckArrayLengths:
    def test_matching_lengths_pass(self):
        check_array_lengths({"x": np.arange(5), "y": np.arange(5)}, "scatter")

    def test_mismatched_raises(self):
        with pytest.raises(ValueError, match="x has 5.*y has 3"):
            check_array_lengths({"x": np.arange(5), "y": np.arange(3)}, "scatter")

    def test_none_values_filtered(self):
        check_array_lengths({"x": np.arange(5), "y": np.arange(5), "size": None}, "scatter")

    def test_single_array_passes(self):
        check_array_lengths({"x": np.arange(5)}, "histogram")

    def test_empty_arrays_pass(self):
        check_array_lengths({"x": np.array([]), "y": np.array([])}, "scatter")

    def test_three_way_mismatch(self):
        with pytest.raises(ValueError, match="array length mismatch"):
            check_array_lengths(
                {"x": np.arange(5), "y": np.arange(3), "size": np.arange(4)},
                "scatter",
            )


# ── check_numeric ────────────────────────────────────────────────────

class TestCheckNumeric:
    def test_int_passes(self):
        check_numeric(np.array([1, 2, 3]), "x", "histogram")

    def test_float_passes(self):
        check_numeric(np.array([1.0, 2.0]), "x", "histogram")

    def test_string_raises(self):
        with pytest.raises(ValueError, match="must be numeric"):
            check_numeric(np.array(["a", "b"]), "x", "histogram")

    def test_object_raises(self):
        with pytest.raises(ValueError, match="must be numeric"):
            check_numeric(np.array([None, None], dtype=object), "x", "histogram")



# ── check_stroke_dash ───────────────────────────────────────────────

class TestCheckStrokeDash:
    _STYLES = {"solid", "dashed", "dotted", "dashdot"}

    def test_valid_silent(self):
        with warnings.catch_warnings():
            warnings.simplefilter("error")
            check_stroke_dash("solid", self._STYLES)
            check_stroke_dash("dashed", self._STYLES)

    def test_none_silent(self):
        with warnings.catch_warnings():
            warnings.simplefilter("error")
            check_stroke_dash(None, self._STYLES)

    def test_invalid_warns(self):
        with pytest.warns(UserWarning, match="Unknown stroke_dash 'wiggly'"):
            check_stroke_dash("wiggly", self._STYLES)



# ── warn_nan_inf ────────────────────────────────────────────────────

class TestWarnNanInf:
    def test_clean_array_silent(self):
        with warnings.catch_warnings():
            warnings.simplefilter("error")
            warn_nan_inf(np.array([1.0, 2.0, 3.0]), "x", "scatter")

    def test_nan_warns(self):
        with pytest.warns(UserWarning, match="2 NaN"):
            warn_nan_inf(np.array([1.0, np.nan, np.nan]), "y", "scatter")

    def test_inf_warns(self):
        with pytest.warns(UserWarning, match="1 Inf"):
            warn_nan_inf(np.array([1.0, np.inf]), "x", "line")

    def test_int_array_skips(self):
        with warnings.catch_warnings():
            warnings.simplefilter("error")
            warn_nan_inf(np.array([1, 2, 3]), "x", "scatter")


# ── validation coverage in marks that previously skipped the helpers ──

class TestValidationCoverage:
    def test_pointplot_length_mismatch_raises(self):
        chart = gufo.chart({"x": ["a", "b", "c"], "y": [1, 2]}).pointplot("x", "y")
        with pytest.raises(ValueError, match=r"pointplot\(\): array length mismatch"):
            chart._render()

    def test_pointplot_nan_warns(self):
        chart = gufo.chart({"x": ["a", "a", "b"], "y": [1.0, np.nan, 3.0]}).pointplot("x", "y")
        with pytest.warns(UserWarning, match=r"pointplot\(\): 'y' contains 1 NaN"):
            chart._render()

    def test_pointplot_clean_data_silent(self):
        chart = gufo.chart({"x": ["a", "a", "b"], "y": [1.0, 2.0, 3.0]}).pointplot("x", "y")
        with warnings.catch_warnings():
            warnings.simplefilter("error")
            chart._render()

    def test_heatmap_long_form_length_mismatch_raises(self):
        data = {"x": ["a", "b", "c"], "y": ["p", "q", "r"], "v": [1, 2]}
        chart = gufo.chart(data).heatmap("x", "y", color="v")
        with pytest.raises(ValueError, match=r"heatmap\(\): array length mismatch"):
            chart._render()

    def test_heatmap_long_form_matching_lengths_render(self):
        data = {"x": ["a", "b"], "y": ["p", "q"], "v": [1, 2]}
        fig, ax = gufo.chart(data).heatmap("x", "y", color="v")._render()
        assert ax.images[0].get_array().shape == (2, 2)

    def test_rug_nan_warns(self):
        chart = gufo.chart({"x": [1.0, np.nan, 3.0]}).rug("x")
        with pytest.warns(UserWarning, match=r"rug\(\): 'x' contains 1 NaN"):
            chart._render()

    def test_rug_clean_data_silent(self):
        chart = gufo.chart({"x": [1.0, 2.0, 3.0]}).rug("x")
        with warnings.catch_warnings():
            warnings.simplefilter("error")
            chart._render()

    def test_rug_string_x_still_renders(self):
        gufo.chart({"x": ["a", "b", "a"]}).rug("x")._render()

    def test_rug_datetime_x_still_renders(self):
        x = np.array(["2020-01-01", "2020-02-01"], dtype="datetime64[D]")
        gufo.chart({"x": x}).rug("x")._render()
