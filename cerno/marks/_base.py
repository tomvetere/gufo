"""Shared utilities for mark renderers."""
from ..style.color import CERNO_PALETTE


def resolve_color(adapter, color_enc):
    """Resolve a color encoding: try as column name, fall back to literal.

    Returns resolved column data (numpy array) or the literal color value.
    Returns None if color_enc is None.
    """
    if color_enc is None:
        return None
    if not isinstance(color_enc, str):
        return color_enc
    try:
        return adapter.resolve(color_enc)
    except (KeyError, TypeError, ValueError):
        return color_enc


def default_colors(n):
    """Return n colors from the cerno palette, cycling if needed."""
    palette = CERNO_PALETTE.categorical
    k = len(palette)
    return [palette[i % k] for i in range(n)]


def apply_label(kwargs, enc):
    """Copy the label encoding into kwargs if present."""
    if enc.get("label") is not None:
        kwargs["label"] = enc["label"]


def apply_color(kwargs, adapter, enc):
    """Resolve and apply a non-categorical color encoding to kwargs."""
    color_value = resolve_color(adapter, enc.get("color"))
    if color_value is not None:
        kwargs["color"] = color_value
    return color_value


def iter_color_groups(color_value):
    """Yield (category, color, mask) for each group in a categorical color array.

    Returns None if color_value is not categorical, allowing callers to
    fall through to the non-grouped code path.
    """
    from ..data.inference import is_categorical
    if color_value is None or not hasattr(color_value, "__len__") or not is_categorical(color_value):
        return None
    categories = list(dict.fromkeys(color_value))
    colors = default_colors(len(categories))
    return [(cat, colors[i], color_value == cat) for i, cat in enumerate(categories)]
