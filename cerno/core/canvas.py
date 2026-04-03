"""Canvas — manages the matplotlib figure and axes lifecycle."""


class Canvas:
    """
    Owns the matplotlib Figure and Axes for a Chart.

    Created lazily at render time so that figsize and theme can be applied
    before any drawing occurs.
    """

    def __init__(self, figsize=None):
        self._figsize = figsize
        self._figure = None
        self._axes = None

    @classmethod
    def from_existing(cls, figure, axes):
        """Wrap an already-created figure and axes (used by Grid)."""
        canvas = cls.__new__(cls)
        canvas._figsize = None
        canvas._figure = figure
        canvas._axes = axes
        return canvas

    def build(self):
        """Create the figure and axes. Called once at render time."""
        if self._figure is not None:
            return self._figure, self._axes
        import matplotlib.pyplot as plt
        self._figure, self._axes = plt.subplots(figsize=self._figsize)
        return self._figure, self._axes
