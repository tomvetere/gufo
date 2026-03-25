import matplotlib.pyplot as plt

THEMES = {
    "neptune_modern": {
        "axes.facecolor": "#f0f0f0",
        "figure.facecolor": "#ffffff",
        "axes.grid": True,
        "grid.color": "#ffffff",
        "grid.linewidth": 1.5,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.spines.bottom": False,
        "axes.spines.left": False,
        "lines.linewidth": 2.5,
        "font.family": "sans-serif",
    }
}

def set_theme(name="neptune_modern"):
    """
    Apply a Neptune theme to the global matplotlib state.
    
    Args:
        name (str): The name of the theme to apply.
    """
    if name in THEMES:
        # In a real implementation, we would merge with default MPL params
        # or use plt.style.use() if we registered them as mpl styles.
        # For now, we update rcParams manually.
        plt.rcParams.update(THEMES[name])
    else:
        print(f"Theme '{name}' not found. Using default.")
