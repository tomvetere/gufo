"""Column type inference — helps marks choose scales and palettes automatically."""
import numpy as np


def is_categorical(arr):
    """Return True if arr should be treated as a categorical variable."""
    if hasattr(arr, "dtype"):
        return arr.dtype.kind in ("O", "U", "S", "b") or str(arr.dtype) == "category"
    if len(arr) == 0:
        return False
    return isinstance(arr[0], (str, bool))


def is_numeric(arr):
    """Return True if arr has a numeric dtype (integer, unsigned, float, or complex)."""
    return np.asarray(arr).dtype.kind in ("i", "u", "f", "c")
