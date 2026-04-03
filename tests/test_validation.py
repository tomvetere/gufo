"""Tests for cerno.core.validate — input validation helpers."""
import warnings

import numpy as np
import pytest

from cerno.core.validate import (
    check_alpha,
    check_array_lengths,
    check_limit_order,
    check_numeric,
    check_positive_dimensions,
    check_scale,
    check_stroke_dash,
    check_ticks_labels,
    check_xy_tuple,
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


# ── check_alpha ──────────────────────────────────────────────────────

class TestCheckAlpha:
    def test_zero_passes(self):
        check_alpha(0)

    def test_one_passes(self):
        check_alpha(1)

    def test_half_passes(self):
        check_alpha(0.5)

    def test_negative_raises(self):
        with pytest.raises(ValueError, match="between 0 and 1"):
            check_alpha(-0.1)

    def test_above_one_raises(self):
        with pytest.raises(ValueError, match="between 0 and 1"):
            check_alpha(1.5)

    def test_non_numeric_raises(self):
        with pytest.raises(ValueError, match="must be a number"):
            check_alpha("half")


# ── check_positive_dimensions ────────────────────────────────────────

class TestCheckPositiveDimensions:
    def test_positive_passes(self):
        check_positive_dimensions(10, 6)

    def test_zero_width_raises(self):
        with pytest.raises(ValueError, match="positive numbers"):
            check_positive_dimensions(0, 5)

    def test_negative_height_raises(self):
        with pytest.raises(ValueError, match="positive numbers"):
            check_positive_dimensions(10, -1)


# ── check_limit_order ────────────────────────────────────────────────

class TestCheckLimitOrder:
    def test_ordered_passes(self):
        check_limit_order(0, 10, "x")

    def test_equal_passes(self):
        check_limit_order(5, 5, "x")

    def test_swapped_raises(self):
        with pytest.raises(ValueError, match="Did you swap"):
            check_limit_order(10, 5, "x")


# ── check_ticks_labels ──────────────────────────────────────────────

class TestCheckTicksLabels:
    def test_matching_passes(self):
        check_ticks_labels([1, 2, 3], ["a", "b", "c"], "x")

    def test_mismatched_raises(self):
        with pytest.raises(ValueError, match="3 ticks but 2 labels"):
            check_ticks_labels([1, 2, 3], ["a", "b"], "x")

    def test_labels_none_skips(self):
        check_ticks_labels([1, 2, 3], None, "x")

    def test_ticks_none_skips(self):
        check_ticks_labels(None, ["a", "b"], "x")


# ── check_xy_tuple ──────────────────────────────────────────────────

class TestCheckXyTuple:
    def test_two_tuple_passes(self):
        check_xy_tuple((1, 2), "annotate")

    def test_two_list_passes(self):
        check_xy_tuple([1, 2], "annotate")

    def test_three_elements_raises(self):
        with pytest.raises(ValueError, match="length 3"):
            check_xy_tuple((1, 2, 3), "annotate")

    def test_non_sequence_raises(self):
        with pytest.raises(ValueError, match="got int"):
            check_xy_tuple(42, "annotate")


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


# ── check_scale ─────────────────────────────────────────────────────

class TestCheckScale:
    def test_log_passes(self):
        check_scale("log", "x")

    def test_linear_passes(self):
        check_scale("linear", "y")

    def test_unknown_raises(self):
        with pytest.raises(ValueError, match="unknown scale 'logs'"):
            check_scale("logs", "x")


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
