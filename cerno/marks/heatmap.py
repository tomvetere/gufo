"""Heatmap mark."""
import numpy as np


def render(layer, adapter, axes):
    enc = layer.encodings
    kwargs = dict(layer.kwargs)

    if layer.x is None and layer.y is None:
        matrix, x_labels, y_labels = _resolve_matrix_form(adapter)
    else:
        matrix, x_labels, y_labels = _resolve_long_form(layer, adapter, enc)

    cmap = enc.get("cmap")
    if cmap is not None:
        kwargs["cmap"] = cmap

    kwargs.setdefault("aspect", "auto")

    im = axes.imshow(matrix, **kwargs)

    axes.set_xticks(range(len(x_labels)), labels=x_labels)
    axes.set_yticks(range(len(y_labels)), labels=y_labels)

    fig = axes.get_figure()
    fig.colorbar(im, ax=axes)

    if enc.get("annotate"):
        _annotate_cells(axes, matrix)


def _resolve_matrix_form(adapter):
    """Extract matrix, x-labels, and y-labels from a DataFrame."""
    data = adapter.raw_data
    if adapter.data_type == "dataframe":
        matrix = data.values.astype(float)
        x_labels = list(data.columns)
        y_labels = list(data.index)
    elif adapter.data_type == "polars":
        matrix = data.to_numpy().astype(float)
        x_labels = list(data.columns)
        y_labels = list(range(len(data)))
    else:
        raise ValueError(
            "Matrix-form heatmap requires a DataFrame. "
            "Pass x, y, and color columns for long-form data."
        )
    return matrix, x_labels, y_labels


def _resolve_long_form(layer, adapter, enc):
    """Pivot long-form x, y, color columns into a matrix."""
    color_col = enc.get("color")
    if color_col is None:
        raise ValueError(
            "Long-form heatmap requires a color encoding. "
            "Use cerno.chart(df).heatmap('x', 'y', color='value_col')."
        )

    x = adapter.resolve(layer.x)
    y = adapter.resolve(layer.y)
    values = adapter.resolve(color_col)

    unique_x = list(dict.fromkeys(x))
    unique_y = list(dict.fromkeys(y))

    matrix = np.full((len(unique_y), len(unique_x)), np.nan)
    x_idx = {v: i for i, v in enumerate(unique_x)}
    y_idx = {v: i for i, v in enumerate(unique_y)}

    for xi, yi, val in zip(x, y, values):
        matrix[y_idx[yi], x_idx[xi]] = val

    return matrix, unique_x, unique_y


def _annotate_cells(axes, matrix):
    """Add text annotations to each cell of the heatmap."""
    rows, cols = matrix.shape
    for i in range(rows):
        for j in range(cols):
            val = matrix[i, j]
            if np.isfinite(val):
                text = str(int(val)) if float(val).is_integer() else f"{val:.2g}"
                axes.text(j, i, text, ha="center", va="center", fontsize="small")
