"""DataAdapter — single resolution point for all input data types."""
import numpy as np
import pandas as pd


class DataAdapter:
    """
    Wraps any supported input data into a common interface.

    Marks never receive raw DataFrames or dicts. They call
    DataAdapter.resolve(key) and get back a numpy array.

    Supported input types:
        pandas.DataFrame  — column access by string key
        dict              — key access
        None              — no bound data; x/y must be arrays/lists directly
    """

    def __init__(self, data):
        self._data = data
        self._type = self._detect_type(data)

    @classmethod
    def from_any(cls, data):
        return cls(data)

    def _detect_type(self, data):
        if data is None:
            return "none"
        if isinstance(data, pd.DataFrame):
            return "dataframe"
        if isinstance(data, dict):
            return "dict"
        raise TypeError(
            f"Unsupported data type: {type(data).__name__}. "
            "Pass a pandas DataFrame, a dict, or None."
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

    def _resolve_column(self, name):
        if self._type in ("dataframe", "dict"):
            return np.asarray(self._data[name])
        raise ValueError(
            f"Cannot resolve column '{name}' — no DataFrame or dict was provided. "
            "Pass data to cerno.chart(data) or pass arrays directly."
        )
