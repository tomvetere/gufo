"""Histogram mark."""
from ..core.validate import check_numeric, warn_nan_inf
from ._base import apply_color, apply_label, iter_color_groups, resolve_color


def render(layer, adapter, axes):
    x = adapter.resolve(layer.x)
    enc = layer.encodings
    kwargs = dict(layer.kwargs)

    check_numeric(x, "x", "histogram")
    warn_nan_inf(x, "x", "histogram")

    kwargs["bins"] = enc.get("bins", "auto")
    kwargs["density"] = enc.get("density", False)

    if enc.get("horizontal"):
        kwargs["orientation"] = "horizontal"

    color_value = resolve_color(adapter, enc.get("color"))
    groups = iter_color_groups(color_value, palette=layer.palette)

    patches = None
    if groups is not None:
        alpha = kwargs.pop("alpha", 0.6)
        for cat, color, mask in groups:
            axes.hist(x[mask], color=color, label=cat, alpha=alpha, **kwargs)
    else:
        apply_label(kwargs, enc)
        apply_color(kwargs, adapter, enc)
        _, _, patches = axes.hist(x, **kwargs)

    kde_config = enc.get("kde")
    if kde_config is not None:
        flat_patches = list(patches) if patches is not None else None
        kde_config.render(x, axes, scale_to_hist=True, hist_patches=flat_patches)
