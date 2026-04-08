"""Input validation helpers for cerno.

Each function checks a single constraint and raises ValueError (or warns)
with a plain-English message that names the problem and suggests a fix.
"""
import warnings

import matplotlib.scale as mscale
import numpy as np


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


def check_numeric(arr, name: str, mark: str):
    """Verify that an array has a numeric dtype."""
    if not hasattr(arr, "dtype"):
        arr = np.asarray(arr)
    if arr.dtype.kind not in ("i", "u", "f", "c"):
        raise ValueError(
            f"{mark}(): '{name}' must be numeric, but got {arr.dtype}. "
            f"{mark.capitalize()} requires numerical data."
        )


def check_alpha(value):
    """Verify that alpha is between 0 and 1."""
    if not isinstance(value, (int, float)):
        raise ValueError(f"alpha must be a number, got {type(value).__name__}.")
    if not 0 <= value <= 1:
        raise ValueError(f"alpha must be between 0 and 1, got {value}.")


def check_positive_dimensions(width, height):
    """Verify that figure dimensions are positive numbers."""
    if width <= 0 or height <= 0:
        raise ValueError(
            f"size() expects positive numbers, got width={width}, height={height}."
        )


def check_limit_order(low, high, axis: str):
    """Verify that the lower limit is less than the upper limit."""
    if low > high:
        raise ValueError(
            f"{axis}lim(): low ({low}) must be less than high ({high}). "
            f"Did you swap the arguments?"
        )


def check_ticks_labels(ticks, labels, axis: str):
    """Verify that ticks and labels have the same length when both provided."""
    if ticks is None or labels is None:
        return
    if len(ticks) != len(labels):
        raise ValueError(
            f"{axis}ticks(): got {len(ticks)} ticks but {len(labels)} labels. "
            f"They must have the same length."
        )


def check_xy_tuple(xy, method: str):
    """Verify that xy is a 2-element sequence."""
    try:
        n = len(xy)
    except TypeError:
        raise ValueError(
            f"{method}(): xy must be an (x, y) pair, got {type(xy).__name__}."
        )
    if n != 2:
        raise ValueError(
            f"{method}(): xy must be an (x, y) pair, got a sequence of length {n}."
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


def check_scale(name: str, axis: str):
    """Verify that the scale name is recognized by matplotlib."""
    valid = mscale.get_scale_names()
    if name not in valid:
        raise ValueError(
            f"{axis}scale(): unknown scale '{name}'. "
            f"Valid scales: {', '.join(sorted(valid))}."
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
