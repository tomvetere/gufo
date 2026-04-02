"""Column type inference — helps marks choose scales and palettes automatically."""
import numpy as np


def is_categorical(arr):
    """Return True if arr should be treated as a categorical variable."""
    if hasattr(arr, "dtype"):
        return arr.dtype.kind in ("O", "U", "S") or str(arr.dtype) == "category"
    if len(arr) == 0:
        return False
    return isinstance(arr[0], str)


def is_datetime(arr):
    """Return True if arr contains datetime values."""
    if hasattr(arr, "dtype"):
        return np.issubdtype(arr.dtype, np.datetime64)
    return False
