"""Tests for cerno.layout — Grid and GridCell."""
import numpy as np
import pytest
import matplotlib.pyplot as plt

import cerno
from cerno.layout.grid import Grid, GridCell, grid
from cerno.core.chart import Chart


# ── Grid construction ───────────────────────────────────────────────

class TestGridConstruction:
    def test_grid_factory(self):
        g = grid(2, 2)
        assert isinstance(g, Grid)

    def test_cerno_grid_entry_point(self):
        g = cerno.grid(2, 2)
        assert isinstance(g, Grid)

    def test_1x1_grid(self):
        g = grid(1, 1)
        cell = g[0, 0]
        assert isinstance(cell, GridCell)

    def test_1x2_grid(self):
        g = grid(1, 2)
        assert isinstance(g[0, 0], GridCell)
        assert isinstance(g[0, 1], GridCell)

    def test_2x1_grid(self):
        g = grid(2, 1)
        assert isinstance(g[0, 0], GridCell)
        assert isinstance(g[1, 0], GridCell)

    def test_2x3_grid(self):
        g = grid(2, 3)
        for r in range(2):
            for c in range(3):
                assert isinstance(g[r, c], GridCell)

    def test_custom_figsize(self):
        g = grid(2, 2, figsize=(14, 10))
        w, h = g._fig.get_size_inches()
        assert w == pytest.approx(14)
        assert h == pytest.approx(10)


# ── GridCell ────────────────────────────────────────────────────────

class TestGridCell:
    def test_cell_returns_chart(self):
        g = grid(2, 2)
        c = g[0, 0].chart()
        assert isinstance(c, Chart)

    def test_cell_chart_with_data(self, sample_df):
        g = grid(1, 1)
        c = g[0, 0].chart(sample_df)
        assert c._data is sample_df

    def test_cell_chart_pre_bound_to_axes(self):
        g = grid(1, 1)
        c = g[0, 0].chart()
        assert c._canvas._built is True
        assert c._canvas._axes is not None
        assert c._canvas._figure is not None

    def test_cell_chart_uses_grid_axes(self):
        g = grid(2, 2)
        c = g[0, 1].chart()
        # The chart's axes should be the grid's axes at [0, 1]
        assert c._canvas._axes is g._axs[0, 1]

    def test_cell_chart_renders(self, sample_df, tmp_path):
        g = grid(2, 2)
        g[0, 0].chart(sample_df).scatter("x", "y").title("Top Left")
        g[0, 1].chart(sample_df).line("x", "y").title("Top Right")
        g[1, 0].chart(sample_df).bar("x", "y").title("Bottom Left")
        g[1, 1].chart(sample_df).histogram("x").title("Bottom Right")
        g.save(tmp_path / "grid.png")
        assert (tmp_path / "grid.png").exists()


# ── Grid output ─────────────────────────────────────────────────────

class TestGridOutput:
    def test_save(self, sample_df, tmp_path):
        g = grid(1, 2)
        g[0, 0].chart(sample_df).scatter("x", "y")
        g[0, 1].chart(sample_df).line("x", "y")
        path = tmp_path / "grid_out.png"
        g.save(str(path))
        assert path.exists()
        assert path.stat().st_size > 0

    def test_save_custom_dpi(self, sample_df, tmp_path):
        g = grid(1, 1)
        g[0, 0].chart(sample_df).scatter("x", "y")
        g.save(tmp_path / "grid_dpi.png", dpi=300)
