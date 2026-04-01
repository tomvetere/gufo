"""Layer dataclass — represents one mark registered on a Chart."""
from dataclasses import dataclass, field
from typing import Any


@dataclass
class Layer:
    """
    A single rendering instruction stored by Chart before render time.

    Marks are not drawn immediately when the user calls .scatter(), .line(), etc.
    Instead each call appends a Layer to Chart._layers. All layers are rendered
    together when .show() or .save() is called, after the theme and figure size
    are finalized.
    """
    mark_type: str                  # "scatter" | "line" | "bar" | "histogram"
    x: Any                          # column name, array, or list
    y: Any                          # column name, array, list, or list-of-names (wide)
    encodings: dict = field(default_factory=dict)   # color, size, alpha, label, etc.
    kwargs: dict = field(default_factory=dict)       # raw mpl kwargs passed through
