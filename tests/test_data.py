"""Tests for cerno.data — DataAdapter and inference."""
import numpy as np
import pandas as pd
import polars as pl
import pytest

from cerno.data.adapter import DataAdapter
from cerno.data.inference import is_categorical, is_datetime


# ── DataAdapter construction ────────────────────────────────────────

class TestDataAdapterConstruction:
    def test_from_dataframe(self, sample_df):
        adapter = DataAdapter(sample_df)
        assert adapter._type == "dataframe"

    def test_from_dict(self, sample_dict):
        adapter = DataAdapter(sample_dict)
        assert adapter._type == "dict"

    def test_from_none(self):
        adapter = DataAdapter(None)
        assert adapter._type == "none"

    def test_from_any_delegates(self, sample_df):
        adapter = DataAdapter.from_any(sample_df)
        assert adapter._type == "dataframe"

    def test_unsupported_type_raises(self):
        with pytest.raises(TypeError, match="Unsupported data type"):
            DataAdapter("not a valid data source")

    def test_unsupported_type_list_raises(self):
        with pytest.raises(TypeError, match="Unsupported data type"):
            DataAdapter([1, 2, 3])

    def test_from_polars(self):
        df = pl.DataFrame({"x": [1, 2, 3], "y": [4, 5, 6]})
        adapter = DataAdapter(df)
        assert adapter._type == "polars"


# ── DataAdapter.resolve ─────────────────────────────────────────────

class TestDataAdapterResolve:
    def test_resolve_column_from_dataframe(self, sample_df):
        adapter = DataAdapter(sample_df)
        result = adapter.resolve("x")
        np.testing.assert_array_equal(result, [1, 2, 3, 4, 5])

    def test_resolve_column_from_dict(self, sample_dict):
        adapter = DataAdapter(sample_dict)
        result = adapter.resolve("x")
        np.testing.assert_array_equal(result, [1, 2, 3])

    def test_resolve_returns_numpy(self, sample_df):
        adapter = DataAdapter(sample_df)
        result = adapter.resolve("x")
        assert isinstance(result, np.ndarray)

    def test_resolve_array_directly(self):
        adapter = DataAdapter(None)
        arr = [10, 20, 30]
        result = adapter.resolve(arr)
        np.testing.assert_array_equal(result, arr)

    def test_resolve_numpy_passthrough(self):
        adapter = DataAdapter(None)
        arr = np.array([1.0, 2.0, 3.0])
        result = adapter.resolve(arr)
        np.testing.assert_array_equal(result, arr)

    def test_resolve_none_returns_none(self):
        adapter = DataAdapter(None)
        assert adapter.resolve(None) is None

    def test_resolve_list_of_column_names(self, sample_df):
        adapter = DataAdapter(sample_df)
        result = adapter.resolve(["x", "y"])
        assert isinstance(result, list)
        assert len(result) == 2
        np.testing.assert_array_equal(result[0], [1, 2, 3, 4, 5])
        np.testing.assert_array_equal(result[1], [2, 4, 1, 5, 3])

    def test_resolve_column_no_data_raises(self):
        adapter = DataAdapter(None)
        with pytest.raises(ValueError, match="Cannot resolve column"):
            adapter.resolve("x")

    def test_resolve_missing_column_raises(self, sample_df):
        adapter = DataAdapter(sample_df)
        with pytest.raises(KeyError):
            adapter.resolve("nonexistent")

    def test_resolve_column_from_polars(self):
        df = pl.DataFrame({"x": [1, 2, 3], "y": [4, 5, 6]})
        adapter = DataAdapter(df)
        result = adapter.resolve("x")
        assert isinstance(result, np.ndarray)
        np.testing.assert_array_equal(result, [1, 2, 3])

    def test_resolve_polars_list_of_columns(self):
        df = pl.DataFrame({"x": [1, 2], "y": [3, 4]})
        adapter = DataAdapter(df)
        result = adapter.resolve(["x", "y"])
        assert len(result) == 2
        np.testing.assert_array_equal(result[0], [1, 2])
        np.testing.assert_array_equal(result[1], [3, 4])


# ── is_categorical ──────────────────────────────────────────────────

class TestIsCategorical:
    def test_numpy_object_dtype(self):
        assert is_categorical(np.array(["a", "b", "c"]))

    def test_numpy_numeric_dtype(self):
        assert not is_categorical(np.array([1, 2, 3]))

    def test_numpy_float_dtype(self):
        assert not is_categorical(np.array([1.0, 2.0]))

    def test_pandas_category_dtype(self):
        s = pd.Categorical(["a", "b", "c"])
        assert is_categorical(s)

    def test_plain_list_of_strings(self):
        assert is_categorical(["a", "b", "c"])

    def test_plain_list_of_ints(self):
        assert not is_categorical([1, 2, 3])

    def test_empty_list(self):
        assert not is_categorical([])

    def test_empty_numpy_array(self):
        assert not is_categorical(np.array([]))


# ── is_datetime ─────────────────────────────────────────────────────

class TestIsDatetime:
    def test_datetime64_array(self):
        arr = np.array(["2024-01-01", "2024-01-02"], dtype="datetime64")
        assert is_datetime(arr)

    def test_numeric_array(self):
        assert not is_datetime(np.array([1, 2, 3]))

    def test_plain_list(self):
        assert not is_datetime([1, 2, 3])


# ── Polars end-to-end ──────────────────────────────────────────────

class TestPolarsEndToEnd:
    def test_scatter_with_polars(self, tmp_path):
        import cerno
        df = pl.DataFrame({"x": [1, 2, 3, 4, 5], "y": [2, 4, 1, 5, 3]})
        cerno.chart(df).scatter("x", "y").save(tmp_path / "pl.png")

    def test_polars_subset(self):
        df = pl.DataFrame({"x": [1, 2, 3], "y": [4, 5, 6]})
        adapter = DataAdapter(df)
        mask = pl.Series([True, False, True])
        sub = adapter.subset(mask)
        np.testing.assert_array_equal(sub.resolve("x"), [1, 3])
