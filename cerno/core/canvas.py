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
        self._built = False

    def build(self):
        """Create the figure and axes. Called once at render time."""
        if self._built:
            return self._figure, self._axes
        import matplotlib.pyplot as plt
        self._figure, self._axes = plt.subplots(figsize=self._figsize)
        self._built = True
        return self._figure, self._axes

    @property
    def figure(self):
        return self._figure

    @property
    def axes(self):
        return self._axes
