"""Tests for cerno faceting."""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pytest

import cerno
from cerno.core.chart import Chart, chart


# ── Facet construction ──────────────────────────────────────────────

class TestFacetConstruction:
    def test_facet_returns_chart(self, sample_df):
        c = chart(sample_df).scatter("x", "y").facet("cat")
        assert isinstance(c, Chart)

    def test_facet_no_data_raises(self):
        with pytest.raises(ValueError, match="requires data"):
            chart().scatter([1, 2], [3, 4]).facet("col")

    def test_facet_non_categorical_raises(self, sample_df, tmp_path):
        with pytest.raises(ValueError, match="not categorical"):
            chart(sample_df).scatter("x", "y").facet("x").save(tmp_path / "bad.png")

    def test_chaining_facet_then_title(self, sample_df, tmp_path):
        c = chart(sample_df).scatter("x", "y").facet("cat").title("Title")
        c.save(tmp_path / "chain1.png")
        assert (tmp_path / "chain1.png").exists()

    def test_chaining_title_then_facet(self, sample_df, tmp_path):
        c = chart(sample_df).scatter("x", "y").title("Title").facet("cat")
        c.save(tmp_path / "chain2.png")
        assert (tmp_path / "chain2.png").exists()


# ── Facet rendering ─────────────────────────────────────────────────

class TestFacetRendering:
    def test_basic_facet_saves(self, sample_df, tmp_path):
        path = tmp_path / "facet.png"
        chart(sample_df).scatter("x", "y").facet("cat").save(path)
        assert path.exists()
        assert path.stat().st_size > 0

    def test_correct_subplot_count(self, sample_df):
        c = chart(sample_df).scatter("x", "y").facet("cat")
        fig, axs = c._render()
        visible = [ax for ax in axs.flat if ax.get_visible()]
        assert len(visible) == 2  # "a" and "b"
        plt.close(fig)

    def test_panel_titles_match_categories(self, sample_df):
        c = chart(sample_df).scatter("x", "y").facet("cat")
        fig, axs = c._render()
        titles = [ax.get_title() for ax in axs.flat if ax.get_visible()]
        assert set(titles) == {"a", "b"}
        plt.close(fig)

    def test_scatter_facet(self, sample_df, tmp_path):
        chart(sample_df).scatter("x", "y").facet("cat").save(tmp_path / "s.png")
        assert (tmp_path / "s.png").exists()

    def test_line_facet(self, sample_df, tmp_path):
        chart(sample_df).line("x", "y").facet("cat").save(tmp_path / "l.png")
        assert (tmp_path / "l.png").exists()

    def test_bar_facet(self, sample_df, tmp_path):
        chart(sample_df).bar("x", "y").facet("cat").save(tmp_path / "b.png")
        assert (tmp_path / "b.png").exists()

    def test_histogram_facet(self, sample_df, tmp_path):
        chart(sample_df).histogram("x").facet("cat").save(tmp_path / "h.png")
        assert (tmp_path / "h.png").exists()

    def test_facet_with_color_encoding(self, tmp_path):
        df = pd.DataFrame({
            "x": range(12),
            "y": range(12),
            "group": ["A"] * 4 + ["B"] * 4 + ["C"] * 4,
            "color": ["red", "blue"] * 6,
        })
        path = tmp_path / "color_facet.png"
        chart(df).scatter("x", "y", color="color").facet("group").save(path)
        assert path.exists()

    def test_facet_wrapping(self, tmp_path):
        df = pd.DataFrame({
            "x": range(25),
            "y": range(25),
            "cat": [c for c in "abcde" for _ in range(5)],
        })
        c = chart(df).scatter("x", "y").facet("cat", cols=2)
        fig, axs = c._render()
        assert axs.shape == (3, 2)  # 5 cats, cols=2 → 3 rows
        visible = [ax for ax in axs.flat if ax.get_visible()]
        assert len(visible) == 5
        hidden = [ax for ax in axs.flat if not ax.get_visible()]
        assert len(hidden) == 1
        plt.close(fig)

    def test_dict_data_facet(self, tmp_path):
        data = {
            "x": [1, 2, 3, 4],
            "y": [4, 3, 2, 1],
            "group": ["a", "a", "b", "b"],
        }
        path = tmp_path / "dict_facet.png"
        chart(data).scatter("x", "y").facet("group").save(path)
        assert path.exists()


# ── Facet decorators ────────────────────────────────────────────────

class TestFacetDecorators:
    def test_chart_title_becomes_suptitle(self, sample_df):
        c = chart(sample_df).scatter("x", "y").title("Overall").facet("cat")
        fig, axs = c._render()
        assert fig._suptitle is not None
        assert fig._suptitle.get_text() == "Overall"
        plt.close(fig)

    def test_theme_respected(self, sample_df, tmp_path):
        path = tmp_path / "themed_facet.png"
        (
            chart(sample_df)
            .scatter("x", "y")
            .theme("cerno_dark")
            .facet("cat")
            .save(path)
        )
        assert path.exists()

    def test_apply_runs_per_panel(self, sample_df, tmp_path):
        call_count = []

        def my_func(figure, axes):
            call_count.append(1)

        path = tmp_path / "apply_facet.png"
        chart(sample_df).scatter("x", "y").apply(my_func).facet("cat").save(path)
        # "cat" has 2 unique values → apply should be called twice
        assert len(call_count) == 2

    def test_xlabel_ylabel_applied(self, sample_df):
        c = (
            chart(sample_df)
            .scatter("x", "y")
            .xlabel("X axis")
            .ylabel("Y axis")
            .facet("cat")
        )
        fig, axs = c._render()
        for ax in axs.flat:
            if ax.get_visible():
                assert ax.get_xlabel() == "X axis"
                assert ax.get_ylabel() == "Y axis"
        plt.close(fig)


# ── Two-variable faceting ──────────────────────────────────────────

class TestTwoVariableFacet:
    @pytest.fixture
    def facet_df(self):
        return pd.DataFrame({
            "x": range(12),
            "y": range(12),
            "row_var": ["R1", "R1", "R1", "R1", "R2", "R2",
                        "R2", "R2", "R3", "R3", "R3", "R3"],
            "col_var": ["C1", "C2", "C1", "C2", "C1", "C2",
                        "C1", "C2", "C1", "C2", "C1", "C2"],
        })

    def test_two_var_facet_saves(self, facet_df, tmp_path):
        path = tmp_path / "two_var.png"
        chart(facet_df).scatter("x", "y").facet("col_var", row="row_var").save(path)
        assert path.exists()

    def test_two_var_facet_grid_shape(self, facet_df):
        c = chart(facet_df).scatter("x", "y").facet("col_var", row="row_var")
        fig, axs = c._render()
        assert axs.shape == (3, 2)  # 3 row cats × 2 col cats
        plt.close(fig)

    def test_two_var_facet_column_headers(self, facet_df):
        c = chart(facet_df).scatter("x", "y").facet("col_var", row="row_var")
        fig, axs = c._render()
        # Top row should have column category titles
        top_titles = [axs[0, j].get_title() for j in range(2)]
        assert set(top_titles) == {"C1", "C2"}
        # Other rows should not have titles set by faceting
        for i in range(1, 3):
            for j in range(2):
                assert axs[i, j].get_title() == ""
        plt.close(fig)

    def test_two_var_facet_row_labels(self, facet_df):
        c = chart(facet_df).scatter("x", "y").facet("col_var", row="row_var")
        fig, axs = c._render()
        row_labels = [axs[i, 0].get_ylabel() for i in range(3)]
        assert row_labels == ["R1", "R2", "R3"]
        plt.close(fig)

    def test_two_var_facet_empty_cells_hidden(self, tmp_path):
        df = pd.DataFrame({
            "x": [1, 2, 3, 4],
            "y": [1, 2, 3, 4],
            "row_var": ["R1", "R1", "R2", "R2"],
            "col_var": ["C1", "C1", "C2", "C2"],
        })
        c = chart(df).scatter("x", "y").facet("col_var", row="row_var")
        fig, axs = c._render()
        # R1×C2 and R2×C1 have no data → hidden
        assert not axs[0, 1].get_visible()
        assert not axs[1, 0].get_visible()
        # R1×C1 and R2×C2 have data → visible
        assert axs[0, 0].get_visible()
        assert axs[1, 1].get_visible()
        plt.close(fig)

    def test_row_only_facet(self, facet_df, tmp_path):
        path = tmp_path / "row_only.png"
        c = chart(facet_df).scatter("x", "y").facet(row="row_var")
        c.save(path)
        assert path.exists()
        fig, axs = c._render()
        assert axs.shape == (3, 1)
        plt.close(fig)

    def test_facet_no_args_raises(self, facet_df):
        with pytest.raises(ValueError, match="at least one"):
            chart(facet_df).scatter("x", "y").facet()

    def test_two_var_facet_with_title(self, facet_df):
        c = (chart(facet_df).scatter("x", "y")
             .title("Two-var").facet("col_var", row="row_var"))
        fig, axs = c._render()
        assert fig._suptitle.get_text() == "Two-var"
        plt.close(fig)
