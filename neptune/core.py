import matplotlib.pyplot as plt
import pandas as pd

class Chart:
    """
    The main interface for Neptune charts.
    Wraps Matplotlib axes to provide a fluent, pythonic API.
    """
    def __init__(self, data=None):
        self._data = data
        self._fig, self._ax = plt.subplots()
        self._title = None
        
    def title(self, text):
        """Set the chart title."""
        self._title = text
        self._ax.set_title(text)
        return self

    def scatter(self, x, y, **kwargs):
        """Create a scatter plot."""
        if self._data is not None:
            # Handle pandas dataframe columns
            if isinstance(self._data, pd.DataFrame):
                x_data = self._data[x]
                y_data = self._data[y]
            else:
                x_data = x
                y_data = y
        else:
            x_data = x
            y_data = y
            
        self._ax.scatter(x_data, y_data, **kwargs)
        return self
        
    def show(self):
        """Display the plot."""
        plt.show()

def chart(data=None):
    """Factory function to create a new Chart instance."""
    return Chart(data)

def plot(data=None):
    """Alias for chart."""
    return Chart(data)
