"""Column type inference — helps marks choose scales and palettes automatically."""
import numpy as np


def is_categorical(arr):
    """Return True if arr should be treated as a categorical variable."""
    if not hasattr(arr, "dtype"):
        arr = np.asarray(arr)
    return arr.dtype.kind in ("O", "U", "S", "b") or str(arr.dtype) == "category"


def is_numeric(arr):
    """Return True if arr has a numeric dtype (integer, unsigned, float, or complex)."""
    return np.asarray(arr).dtype.kind in ("i", "u", "f", "c")
