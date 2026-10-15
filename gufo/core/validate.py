"""Input validation helpers for gufo.

Each function checks a single constraint and raises ValueError (or warns)
with a plain-English message that names the problem and suggests a fix.
"""
import warnings

import numpy as np

from ..data.inference import is_numeric


def check_array_lengths(arrays: dict, mark: str):
    """Verify that all provided arrays have the same length."""
    lengths = {name: len(arr) for name, arr in arrays.items() if arr is not None}
    if len(lengths) < 2:
        return
    unique = set(lengths.values())
    if len(unique) == 1:
        return
    detail = ", ".join(f"{name} has {n}" for name, n in lengths.items())
    raise ValueError(
        f"{mark}(): array length mismatch — {detail}. "
        f"All data arrays must have the same length."
    )


def check_error_shape(err, n: int, name: str, mark: str):
    """Verify an error array fits n bars by matplotlib's rule: it broadcasts to (2, n)."""
    if err is None:
        return
    try:
        np.broadcast_to(err, (2, n))
    except ValueError:
        raise ValueError(
            f"{mark}(): array length mismatch — x has {n}, {name} has shape "
            f"{np.shape(err)}. Errors must be a scalar, have one value per bar, "
            f"or have shape (2, {n}) for lower/upper errors."
        ) from None


def check_numeric(arr, name: str, mark: str):
    """Verify that an array has a numeric dtype."""
    arr = np.asarray(arr)
    if not is_numeric(arr):
        raise ValueError(
            f"{mark}(): '{name}' must be numeric, but got {arr.dtype}. "
            f"{mark.capitalize()} requires numerical data."
        )


def check_stroke_dash(name, valid_styles):
    """Warn if the stroke dash style is not recognized.

    Parameters
    ----------
    name : str or None
        The dash style name to check.
    valid_styles : collection
        The set of valid style names (e.g. ``_DASH_STYLES`` keys).
    """
    if name is None:
        return
    if name not in valid_styles:
        warnings.warn(
            f"Unknown stroke_dash '{name}'. "
            f"Valid options: {', '.join(sorted(valid_styles))}. Defaulting to solid.",
            stacklevel=3,
        )


def warn_nan_inf(arr, name: str, mark: str):
    """Warn if a numeric array contains NaN or Inf values."""
    if not hasattr(arr, "dtype") or arr.dtype.kind not in ("f", "c"):
        return
    # Fast path: skip counting if all values are finite.
    if np.isfinite(arr).all():
        return
    nan_count = int(np.isnan(arr).sum())
    inf_count = int(np.isinf(arr).sum())
    if nan_count:
        warnings.warn(
            f"{mark}(): '{name}' contains {nan_count} NaN value(s). "
            f"They will be omitted from the plot.",
            stacklevel=3,
        )
    if inf_count:
        warnings.warn(
            f"{mark}(): '{name}' contains {inf_count} Inf value(s). "
            f"They may cause unexpected plot behavior.",
            stacklevel=3,
        )
