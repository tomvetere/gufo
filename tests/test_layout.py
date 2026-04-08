"""Tests for cerno grid layout."""
import numpy as np
import pytest
import matplotlib.pyplot as plt

import cerno
from cerno.core.chart import Chart, chart
from cerno.layout.grid import Grid


# ── Grid construction ───────────────────────────────────────────────

class TestGridConstruction:
    def test_grid_returns_grid(self):
        g = Grid(2, 2)
        assert isinstance(g, Grid)

    def test_grid_is_not_chart(self):
        g = Grid(2, 2)
        assert not isinstance(g, Chart)

    def test_cerno_grid_entry_point(self):
        g = cerno.grid(2, 2)
        assert isinstance(g, Grid)

    def test_custom_figsize(self, sample_df, tmp_path):
        g = Grid(2, 2, figsize=(14, 10))
        g[0, 0] = chart(sample_df).scatter("x", "y")
        g.save(tmp_path / "sized.png")
        assert (tmp_path / "sized.png").exists()

    def test_setitem_rejects_non_chart(self):
        g = Grid(2, 2)
        with pytest.raises(TypeError, match="Chart instance"):
            g[0, 0] = "not a chart"

    def test_setitem_rejects_out_of_range(self):
        g = Grid(2, 2)
        with pytest.raises(IndexError, match="out of range"):
            g[5, 5] = chart()

    def test_getitem_raises_helpful_error(self):
        g = Grid(2, 2)
        with pytest.raises(TypeError, match="write-only"):
            _ = g[0, 0]


# ── Grid panels ────────────────────────────────────────────────────

class TestGridPanels:
    def test_all_mark_types_render(self, sample_df, tmp_path):
        g = Grid(2, 2)
        g[0, 0] = chart(sample_df).scatter("x", "y").title("Scatter")
        g[0, 1] = chart(sample_df).line("x", "y").title("Line")
        g[1, 0] = chart(sample_df).bar("x", "y").title("Bar")
        g[1, 1] = chart(sample_df).histogram("x").title("Histogram")
        g.save(tmp_path / "grid.png")
        assert (tmp_path / "grid.png").exists()

    def test_different_data_per_panel(self, tmp_path):
        df1 = {"x": [1, 2, 3], "y": [4, 5, 6]}
        df2 = {"x": [10, 20], "y": [30, 40]}
        g = Grid(1, 2)
        g[0, 0] = chart(df1).scatter("x", "y")
        g[0, 1] = chart(df2).bar("x", "y")
        g.save(tmp_path / "multi_data.png")
        assert (tmp_path / "multi_data.png").exists()

    def test_grid_suptitle(self, sample_df, tmp_path):
        g = Grid(1, 2).title("Overall Title")
        g[0, 0] = chart(sample_df).scatter("x", "y")
        g[0, 1] = chart(sample_df).line("x", "y")
        path = tmp_path / "suptitle.png"
        g.save(path)
        assert path.exists()

    def test_empty_cells_hidden(self, sample_df, tmp_path):
        g = Grid(2, 2)
        g[0, 0] = chart(sample_df).scatter("x", "y")
        # Leave other 3 cells empty
        g.save(tmp_path / "sparse.png")
        assert (tmp_path / "sparse.png").exists()

    def test_grid_theme(self, sample_df, tmp_path):
        g = Grid(1, 1).theme("cerno_modern")
        g[0, 0] = chart(sample_df).scatter("x", "y")
        g.save(tmp_path / "themed.png")
        assert (tmp_path / "themed.png").exists()

    def test_grid_apply(self, sample_df, tmp_path):
        called = []

        def my_func(fig, axs):
            called.append(True)

        g = Grid(1, 1).apply(my_func)
        g[0, 0] = chart(sample_df).scatter("x", "y")
        g.save(tmp_path / "apply.png")
        assert len(called) == 1


# ── Grid output ─────────────────────────────────────────────────────

class TestGridOutput:
    def test_save(self, sample_df, tmp_path):
        g = cerno.grid(1, 2)
        g[0, 0] = cerno.chart(sample_df).scatter("x", "y")
        g[0, 1] = cerno.chart(sample_df).line("x", "y")
        path = tmp_path / "grid_out.png"
        g.save(str(path))
        assert path.exists()
        assert path.stat().st_size > 0

    def test_save_custom_dpi(self, sample_df, tmp_path):
        g = cerno.grid(1, 1)
        g[0, 0] = cerno.chart(sample_df).scatter("x", "y")
        g.save(tmp_path / "grid_dpi.png", dpi=300)
