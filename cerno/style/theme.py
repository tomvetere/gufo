"""Theme — immutable style object with registry and context manager support."""
import contextlib
import matplotlib.pyplot as plt


class Theme:
    """
    An immutable description of visual style for a chart.

    Themes do not mutate global state until explicitly applied.
    Use as_context() to scope a theme to a with-block.
    Use apply_global() (or cerno.set_theme()) to set the global default.
    """

    def __init__(self, name, rc):
        self._name = name
        self._rc = dict(rc)

    @property
    def name(self):
        return self._name

    def merge(self, overrides):
        """
        Return a new Theme that is this theme with overrides applied.
        This theme is not modified.
        """
        merged_rc = {**self._rc, **overrides}
        return Theme(self._name, merged_rc)

    def rename(self, name):
        """Return a copy of this theme with a new name."""
        return Theme(name, self._rc)

    @contextlib.contextmanager
    def as_context(self):
        """Scope this theme to a with-block using plt.rc_context."""
        with plt.rc_context(self._rc):
            yield

    def apply_global(self):
        """Apply this theme to matplotlib's global rcParams."""
        plt.rcParams.update(self._rc)


# ---------------------------------------------------------------------------
# Built-in themes
# ---------------------------------------------------------------------------

_CERNO_MODERN_RC = {
    "axes.facecolor": "#f5f5f5",
    "figure.facecolor": "#ffffff",
    "axes.grid": True,
    "grid.color": "#ffffff",
    "grid.linewidth": 1.2,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.spines.left": False,
    "axes.spines.bottom": False,
    "lines.linewidth": 2.0,
    "font.family": "sans-serif",
    "axes.prop_cycle": plt.cycler(color=[
        "#4C72B0", "#DD8452", "#55A868", "#C44E52",
        "#8172B3", "#937860", "#DA8BC3", "#8C8C8C",
    ]),
}

_CERNO_DARK_RC = {
    "axes.facecolor": "#1e1e2e",
    "figure.facecolor": "#13131e",
    "axes.grid": True,
    "grid.color": "#2e2e4e",
    "grid.linewidth": 1.0,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.spines.left": False,
    "axes.spines.bottom": False,
    "lines.linewidth": 2.0,
    "text.color": "#cccccc",
    "axes.labelcolor": "#cccccc",
    "xtick.color": "#cccccc",
    "ytick.color": "#cccccc",
    "font.family": "sans-serif",
}

_CERNO_PRINT_RC = {
    "axes.facecolor": "#ffffff",
    "figure.facecolor": "#ffffff",
    "axes.grid": True,
    "grid.color": "#cccccc",
    "grid.linewidth": 0.8,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "lines.linewidth": 1.5,
    "font.family": "serif",
    "axes.prop_cycle": plt.cycler(color=[
        "#000000", "#444444", "#888888", "#bbbbbb",
    ]),
}

# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------

_REGISTRY: dict = {}


def register_theme(theme: Theme) -> None:
    """Register a Theme so it can be referenced by name."""
    _REGISTRY[theme.name] = theme


def get_theme(name: str) -> Theme:
    """Return the Theme registered under name."""
    if name not in _REGISTRY:
        available = list(_REGISTRY)
        raise ValueError(f"Unknown theme '{name}'. Available: {available}")
    return _REGISTRY[name]


def set_theme(name: str = "cerno_modern") -> None:
    """Apply a theme globally to all subsequent charts."""
    get_theme(name).apply_global()


@contextlib.contextmanager
def theme_context(name: str):
    """Temporarily apply a theme within a with-block."""
    with get_theme(name).as_context():
        yield


def _resolve_theme(override):
    """Internal: return the Theme to use for a single render call."""
    if override is None:
        # Return a no-op theme that applies nothing new
        return Theme("_passthrough", {})
    if isinstance(override, str):
        return get_theme(override)
    if isinstance(override, Theme):
        return override
    raise TypeError(f"theme() expects a theme name (str) or Theme object, got {type(override)}")


# Register built-ins at import time
register_theme(Theme("cerno_modern", _CERNO_MODERN_RC))
register_theme(Theme("cerno_dark", _CERNO_DARK_RC))
register_theme(Theme("cerno_print", _CERNO_PRINT_RC))
