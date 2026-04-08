"""Tests for cerno.core.validate — input validation helpers."""
import warnings

import numpy as np
import pytest

from cerno.core.validate import (
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
