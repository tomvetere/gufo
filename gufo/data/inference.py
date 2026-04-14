"""Column type inference — helps marks choose scales and palettes automatically."""


def is_categorical(arr):
    """Return True if arr should be treated as a categorical variable."""
    if hasattr(arr, "dtype"):
        return arr.dtype.kind in ("O", "U", "S") or str(arr.dtype) == "category"
    if len(arr) == 0:
        return False
    return isinstance(arr[0], str)
