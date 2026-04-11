"""DataAdapter — single resolution point for all input data types."""
import numpy as np

try:
    import pandas as pd
except ImportError:
    pd = None

try:
    import polars as pl
except ImportError:
    pl = None


class DataAdapter:
    """
    Wraps any supported input data into a common interface.

    Marks never receive raw DataFrames or dicts. They call
    DataAdapter.resolve(key) and get back a numpy array.

    Supported input types:
        pandas.DataFrame  — column access by string key
        polars.DataFrame  — column access by string key (optional dependency)
        dict              — key access
        None              — no bound data; x/y must be arrays/lists directly
    """

    def __init__(self, data):
        self._data = data
        self._type = self._detect_type(data)

    @property
    def raw_data(self):
        """The original data object passed to the adapter."""
        return self._data

    @property
    def data_type(self):
        """String identifying the data backend: 'dataframe', 'polars', 'dict', or 'none'."""
        return self._type

    @classmethod
    def from_any(cls, data):
        return cls(data)

    def _detect_type(self, data):
        if data is None:
            return "none"
        if pd is not None and isinstance(data, pd.DataFrame):
            return "dataframe"
        if pl is not None and isinstance(data, pl.DataFrame):
            return "polars"
        # Fallback: detect by module name when library import failed
        cls_module = type(data).__module__ or ""
        cls_name = type(data).__qualname__
        if cls_name == "DataFrame":
            if cls_module.startswith("pandas"):
                return "dataframe"
            if cls_module.startswith("polars"):
                return "polars"
        if isinstance(data, dict):
            return "dict"
        supported = ["pandas DataFrame", "Polars DataFrame", "dict", "None"]
        raise TypeError(
            f"Unsupported data type: {type(data).__name__}. "
            f"Pass a {', '.join(supported[:-1])}, or {supported[-1]}."
        )

    def column_names(self):
        """Return list of column names from bound data."""
        if self._type in ("dataframe", "polars"):
            return list(self._data.columns)
        if self._type == "dict":
            return list(self._data.keys())
        raise ValueError(
            "Cannot list columns — no columnar data was provided. "
            "Pass a DataFrame or dict to cerno.chart(data)."
        )

    def resolve(self, key):
        """
        Return key as a numpy array.

        key may be:
            str           — column name looked up in bound data
            list of str   — multiple columns (wide-form); returns list of arrays
            array-like    — returned as numpy array directly
        """
        if isinstance(key, str):
            return self._resolve_column(key)
        if isinstance(key, list):
            if all(isinstance(k, str) for k in key):
                return [self._resolve_column(k) for k in key]
            return [np.asarray(k) for k in key]
        if key is None:
            return None
        return np.asarray(key)

    def subset(self, mask):
        """Return a new DataAdapter containing only rows where mask is True."""
        if self._type == "none":
            raise ValueError(
                "Cannot subset data — no DataFrame or dict was provided. "
                "Faceting requires bound columnar data passed to cerno.chart(data)."
            )
        if self._type == "dataframe":
            return DataAdapter(self._data[mask].reset_index(drop=True))
        if self._type == "polars":
            return DataAdapter(self._data.filter(mask))
        if self._type == "dict":
            filtered = {k: np.asarray(v)[mask] for k, v in self._data.items()}
            return DataAdapter(filtered)

    def _resolve_column(self, name):
        if self._type in ("dataframe", "dict"):
            return np.asarray(self._data[name])
        if self._type == "polars":
            return self._data[name].to_numpy()
        raise ValueError(
            f"Cannot resolve column '{name}' — no DataFrame or dict was provided. "
            "Pass data to cerno.chart(data) or pass arrays directly."
        )
