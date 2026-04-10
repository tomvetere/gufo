"""Strip mark — jittered points along a categorical axis."""

import numpy as np

from ._base import render_categorical_scatter


def _jitter_offsets(values, enc):
    """Generate uniform random jitter offsets."""
    jitter = enc.get("jitter", 0.2)
    rng = np.random.default_rng(42)
    return rng.uniform(-jitter, jitter, size=len(values))


def render(layer, adapter, axes):
    render_categorical_scatter(
        layer, adapter, axes, _jitter_offsets, "strip",
        default_alpha=0.6, default_size=20,
    )
