"""Palette abstraction — categorical, sequential, and diverging color sets."""
from dataclasses import dataclass
from typing import List


@dataclass
class Palette:
    categorical: List[str]
    sequential: List[str]
    diverging: List[str]


CERNO_PALETTE = Palette(
    categorical=["#4C72B0", "#DD8452", "#55A868", "#C44E52",
                 "#8172B3", "#937860", "#DA8BC3", "#8C8C8C"],
    sequential=["#f7fbff", "#c6dbef", "#6baed6", "#2171b5", "#08306b"],
    diverging=["#d73027", "#f46d43", "#fdae61", "#fee090",
               "#e0f3f8", "#abd9e9", "#74add1", "#313695"],
)
