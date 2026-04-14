"""Mark rendering — one module per chart type."""
from .area import render as _area
from .bar import render as _bar
from .boxplot import render as _boxplot
from .countplot import render as _countplot
from .ecdf import render as _ecdf
from .heatmap import render as _heatmap
from .histogram import render as _histogram
from .kde import render as _kde
from .line import render as _line
from .pointplot import render as _pointplot
from .rug import render as _rug
from .scatter import render as _scatter
from .strip import render as _strip
from .swarm import render as _swarm
from .violin import render as _violin

_REGISTRY = {
    "scatter": _scatter,
    "line": _line,
    "bar": _bar,
    "histogram": _histogram,
    "boxplot": _boxplot,
    "violin": _violin,
    "heatmap": _heatmap,
    "area": _area,
    "kde": _kde,
    "strip": _strip,
    "swarm": _swarm,
    "countplot": _countplot,
    "ecdf": _ecdf,
    "rug": _rug,
    "pointplot": _pointplot,
}


def render_layer(layer, adapter, axes):
    """Dispatch a Layer to the correct mark renderer."""
    renderer = _REGISTRY.get(layer.mark_type)
    if renderer is None:
        raise ValueError(f"Unknown mark type: '{layer.mark_type}'")
    renderer(layer, adapter, axes)
