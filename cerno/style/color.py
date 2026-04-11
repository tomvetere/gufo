"""Palette abstraction — categorical, sequential, and diverging color sets."""
from dataclasses import dataclass


@dataclass
class Palette:
    categorical: list[str]
    sequential: list[str]
    diverging: list[str]


CERNO_PALETTE = Palette(
    categorical=["#4C72B0", "#DD8452", "#55A868", "#C44E52",
                 "#8172B3", "#937860", "#DA8BC3", "#8C8C8C"],
    sequential=["#f7fbff", "#c6dbef", "#6baed6", "#2171b5", "#08306b"],
    diverging=["#d73027", "#f46d43", "#fdae61", "#fee090",
               "#e0f3f8", "#abd9e9", "#74add1", "#313695"],
)

NAMED_PALETTES = {
    "cerno": CERNO_PALETTE.categorical,
    "pastel": ["#A1C9F4", "#FFB482", "#8DE5A1", "#FF9F9B",
               "#D0BBFF", "#DEBB9B", "#FAB0E4", "#CFCFCF"],
    "bold": ["#1B9E77", "#D95F02", "#7570B3", "#E7298A",
             "#66A61E", "#E6AB02", "#A6761D", "#666666"],
    "colorblind": ["#0173B2", "#DE8F05", "#029E73", "#D55E00",
                   "#CC78BC", "#CA9161", "#FBAFE4", "#949494"],
}


def resolve_palette(palette):
    """Resolve a palette argument to a list of color strings.

    Accepts None (default cerno palette), a string name from
    NAMED_PALETTES, or a list of color strings passed through directly.
    """
    if palette is None:
        return CERNO_PALETTE.categorical
    if isinstance(palette, str):
        if palette not in NAMED_PALETTES:
            raise ValueError(
                f"Unknown palette '{palette}'. "
                f"Available: {sorted(NAMED_PALETTES)}"
            )
        return NAMED_PALETTES[palette]
    return list(palette)
