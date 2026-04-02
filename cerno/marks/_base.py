"""Shared utilities for mark renderers."""


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
    """Return n colors from the tab10 colormap."""
    import matplotlib.pyplot as plt
    cmap = plt.get_cmap("tab10")
    return [cmap(i % 10) for i in range(n)]
