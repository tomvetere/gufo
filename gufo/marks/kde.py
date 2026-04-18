"""KDE mark — standalone density plot."""

from dataclasses import replace

from ..core.validate import check_numeric, warn_nan_inf
from ..stats.kde import KDE as KDEConfig
from ._base import resolve_color, iter_color_groups


def render(layer, adapter, axes):
    x = adapter.resolve(layer.x)
    enc = layer.encodings
    extra_kwargs = dict(layer.kwargs)

    check_numeric(x, "x", "kde")
    warn_nan_inf(x, "x", "kde")

    kde_config = enc.get("kde_config")
    if kde_config is None:
        kde_config = KDEConfig()

    color_value = resolve_color(adapter, enc.get("color"))
    groups = iter_color_groups(color_value, palette=layer.palette,
                               color_order=enc.get("color_order"))

    if groups is not None:
        for cat, color, mask in groups:
            group_kde = replace(kde_config, color=color, label=cat)
            group_kde.render(x[mask], axes, **extra_kwargs)
        return

    overrides = {}
    if color_value is not None and kde_config.color is None:
        overrides["color"] = color_value
    if enc.get("label") is not None and kde_config.label is None:
        overrides["label"] = enc["label"]

    if overrides:
        kde_config = replace(kde_config, **overrides)

    kde_config.render(x, axes, **extra_kwargs)
