"""Tests for gufo pair plot."""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pytest

import gufo
from gufo.layout.grid import Grid


@pytest.fixture
def iris_df():
    """A small DataFrame with numeric and categorical columns."""
    np.random.seed(42)
    n = 30
    return pd.DataFrame({
        "sepal_length": np.random.normal(5.8, 0.8, n),
        "sepal_width": np.random.normal(3.0, 0.4, n),
        "petal_length": np.random.normal(3.7, 1.7, n),
        "species": np.random.choice(["setosa", "versicolor", "virginica"], n),
    })


@pytest.fixture
def numeric_df():
    """A DataFrame with only numeric columns."""
    np.random.seed(0)
    return pd.DataFrame({
        "a": np.random.randn(20),
        "b": np.random.randn(20),
        "c": np.random.randn(20),
    })


class TestPairplotConstruction:
    def test_returns_grid(self, numeric_df):
        g = gufo.pairplot(numeric_df)
        assert isinstance(g, Grid)

    def test_correct_grid_shape(self, numeric_df):
        g = gufo.pairplot(numeric_df)
        fig, axs = g._render()
        assert axs.shape == (3, 3)
        plt.close(fig)

    def test_excludes_categorical(self, iris_df):
        g = gufo.pairplot(iris_df)
        fig, axs = g._render()
        # 3 numeric columns (species excluded)
        assert axs.shape == (3, 3)
        plt.close(fig)

    def test_column_subset(self, numeric_df):
        g = gufo.pairplot(numeric_df, columns=["a", "b"])
        fig, axs = g._render()
        assert axs.shape == (2, 2)
        plt.close(fig)

    def test_too_few_columns_raises(self):
        df = pd.DataFrame({"x": [1, 2, 3], "cat": ["a", "b", "c"]})
        with pytest.raises(ValueError, match="at least 2"):
            gufo.pairplot(df)

    def test_no_data_raises(self):
        with pytest.raises((TypeError, ValueError)):
            gufo.pairplot(None)


class TestPairplotRendering:
    def test_saves(self, numeric_df, tmp_path):
        path = tmp_path / "pairplot.png"
        gufo.pairplot(numeric_df).save(path)
        assert path.exists()
        assert path.stat().st_size > 0

    def test_diagonal_has_histograms(self, numeric_df):
        g = gufo.pairplot(numeric_df)
        fig, axs = g._render()
        for i in range(3):
            patches = axs[i, i].patches
            assert len(patches) > 0, f"Diagonal cell [{i},{i}] has no histogram"
        plt.close(fig)

    def test_offdiag_has_scatter(self, numeric_df):
        g = gufo.pairplot(numeric_df)
        fig, axs = g._render()
        # Check a few off-diagonal cells for PathCollections (scatter)
        for i, j in [(0, 1), (1, 0), (0, 2)]:
            collections = axs[i, j].collections
            assert len(collections) > 0, f"Off-diagonal [{i},{j}] has no scatter"
        plt.close(fig)

    def test_with_color(self, iris_df, tmp_path):
        path = tmp_path / "pair_color.png"
        gufo.pairplot(iris_df, color="species").save(path)
        assert path.exists()

    def test_axis_labels(self, numeric_df):
        g = gufo.pairplot(numeric_df)
        fig, axs = g._render()
        n = 3
        cols = ["a", "b", "c"]
        # Bottom row should have x-labels
        for j in range(n):
            assert axs[n - 1, j].get_xlabel() == cols[j]
        # Left column should have y-labels
        for i in range(n):
            assert axs[i, 0].get_ylabel() == cols[i]
        plt.close(fig)

    def test_title(self, numeric_df):
        g = gufo.pairplot(numeric_df).title("Pair Plot")
        fig, axs = g._render()
        assert fig._suptitle is not None
        assert fig._suptitle.get_text() == "Pair Plot"
        plt.close(fig)

    def test_custom_figsize(self, numeric_df):
        g = gufo.pairplot(numeric_df, figsize=(12, 12))
        fig, axs = g._render()
        w, h = fig.get_size_inches()
        assert w == pytest.approx(12)
        assert h == pytest.approx(12)
        plt.close(fig)


class TestPairplotDataFormats:
    def test_dict_data(self, tmp_path):
        data = {"x": [1, 2, 3, 4], "y": [4, 3, 2, 1], "z": [1, 1, 2, 2]}
        path = tmp_path / "dict_pair.png"
        gufo.pairplot(data).save(path)
        assert path.exists()

    def test_polars_data(self, tmp_path):
        pl = pytest.importorskip("polars")
        df = pl.DataFrame({
            "a": [1.0, 2.0, 3.0, 4.0],
            "b": [4.0, 3.0, 2.0, 1.0],
        })
        path = tmp_path / "polars_pair.png"
        gufo.pairplot(df).save(path)
        assert path.exists()

    def test_color_column_excluded_from_grid(self, iris_df):
        g = gufo.pairplot(iris_df, color="species")
        fig, axs = g._render()
        # species is categorical AND is the color column — grid should be 3x3
        assert axs.shape == (3, 3)
        plt.close(fig)
