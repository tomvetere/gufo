"""Pointplot mark — connected category means with confidence intervals."""
import numpy as np

from ._base import _resolve_order, iter_color_groups, resolve_color, set_category_ticks


def render(layer, adapter, axes):
    enc = layer.encodings
    x = adapter.resolve(layer.x)
    y = adapter.resolve(layer.y)

    x = np.asarray(x)
    y = np.asarray(y, dtype=float)

    horizontal = enc.get("horizontal", False)
    color_value = resolve_color(adapter, enc.get("color"))
    groups = iter_color_groups(color_value, palette=layer.palette,
                               color_order=enc.get("color_order"))

    unique_x = _resolve_order(x, enc.get("order"))
    x_pos = np.arange(len(unique_x))
    x_to_idx = {val: i for i, val in enumerate(unique_x)}
    valid = np.isin(x, unique_x)
    xf, yf = x[valid], y[valid]
    x_indices = np.array([x_to_idx[v] for v in xf])

    kwargs = dict(layer.kwargs)
    kwargs.setdefault("marker", "o")
    kwargs.setdefault("capsize", 4)

    if groups is not None:
        n_groups = len(groups)
        dodge_width = 0.2
        for gi, (cat, color, mask) in enumerate(groups):
            maskf = mask[valid]
            means, cis = _aggregate(yf[maskf], x_indices[maskf], len(unique_x))
            offset = (gi - n_groups / 2 + 0.5) * dodge_width
            _draw(axes, x_pos + offset, means, cis, horizontal,
                  color=color, label=cat, **kwargs)
    else:
        means, cis = _aggregate(yf, x_indices, len(unique_x))
        _draw(axes, x_pos, means, cis, horizontal, **kwargs)

    set_category_ticks(axes, x_pos, unique_x, horizontal)


def _aggregate(y, x_indices, n_categories):
    """Compute means and 95% CI (via standard error) per category."""
    counts = np.bincount(x_indices, minlength=n_categories)
    sums = np.bincount(x_indices, weights=y, minlength=n_categories)
    safe = counts > 0
    means = np.where(safe, sums / np.where(safe, counts, 1), np.nan)
    sum_sq = np.bincount(x_indices, weights=y ** 2, minlength=n_categories)
    safe_denom = np.where(counts > 1, counts - 1, 1)
    variance = np.where(
        counts > 1,
        (sum_sq - sums ** 2 / np.where(safe, counts, 1)) / safe_denom,
        0.0,
    )
    cis = np.where(counts > 1, 1.96 * np.sqrt(variance / counts), 0.0)
    return means, cis


def _draw(axes, positions, means, cis, horizontal, **kwargs):
    """Draw the errorbar + connecting line."""
    if horizontal:
        axes.errorbar(means, positions, xerr=cis, **kwargs)
    else:
        axes.errorbar(positions, means, yerr=cis, **kwargs)
