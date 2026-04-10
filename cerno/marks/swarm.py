"""Swarm mark — beeswarm non-overlapping categorical scatter."""

import numpy as np

from ..stats import _require_scipy
from ._base import render_categorical_scatter


def _swarm_offsets(values, enc):
    """Compute beeswarm offsets to avoid point overlap."""
    size = enc.get("size", 20)
    return _beeswarm_offsets(values, size)


def render(layer, adapter, axes):
    _require_scipy("swarm")
    render_categorical_scatter(
        layer, adapter, axes, _swarm_offsets, "swarm",
        default_alpha=0.7, default_size=20,
    )


def _beeswarm_offsets(values, marker_size, max_width=0.4):
    """Compute categorical-axis offsets to avoid point overlap.

    Uses a greedy algorithm: sort by value, then for each point find the
    minimum offset from center that doesn't collide with already-placed points.
    """
    values = np.asarray(values, dtype=float)
    n = len(values)
    if n == 0:
        return np.array([])

    radius = _estimate_radius(values, marker_size)

    order = np.argsort(values)
    offsets = np.zeros(n)
    placed_vals = []
    placed_offs = []

    for idx in order:
        val = values[idx]
        best_offset = 0.0

        for step in range(n + 1):
            candidate = (step + 1) // 2 * radius * 1.5
            if step % 2 == 1:
                candidate = -candidate

            collision = False
            for pv, po in zip(placed_vals, placed_offs):
                if (abs(val - pv) < radius * 2
                        and abs(candidate - po) < radius * 1.5):
                    collision = True
                    break

            if not collision:
                best_offset = candidate
                break

        best_offset = np.clip(best_offset, -max_width, max_width)
        offsets[idx] = best_offset
        placed_vals.append(val)
        placed_offs.append(best_offset)

    return offsets


def _estimate_radius(values, marker_size):
    """Estimate a collision radius in data-axis units."""
    val_range = np.ptp(values)
    if val_range == 0:
        return 0.05
    point_radius = np.sqrt(marker_size) / 2
    return val_range * point_radius / 400
