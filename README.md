# Neptune

**Data Visualization, Humanized.**

Neptune is a Python library built on top of Matplotlib that prioritizes:
1.  **Usability**: A fluent, method-chaining API.
2.  **Aesthetics**: Modern, clean defaults.
3.  **Integration**: Seamless work with Pandas and Jupyter.

## Quick Start

```python
import neptune
import pandas as pd

# Apply modern look
neptune.set_theme()

df = pd.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]})

# Fluent API
neptune.chart(df).scatter('a', 'b').title("My First Neptune Plot").show()
```
