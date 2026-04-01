"""Mark rendering — one module per chart type."""
from .scatter import render as _scatter
from .line import render as _line
from .bar import render as _bar
from .histogram import render as _histogram

_REGISTRY = {
    "scatter": _scatter,
    "line": _line,
    "bar": _bar,
    "histogram": _histogram,
}


def render_layer(layer, data, axes):
    """Dispatch a Layer to the correct mark renderer."""
    from ..data.adapter import DataAdapter
    adapter = DataAdapter.from_any(data)
    renderer = _REGISTRY.get(layer.mark_type)
    if renderer is None:
        raise ValueError(f"Unknown mark type: '{layer.mark_type}'")
    renderer(layer, adapter, axes)
