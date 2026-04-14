"""Shared fixtures for gufo tests."""
import matplotlib
matplotlib.use("Agg")  # non-interactive backend for CI

import matplotlib.pyplot as plt
import pytest
import numpy as np
import pandas as pd


@pytest.fixture(autouse=True)
def _close_figures():
    """Close all matplotlib figures after each test."""
    yield
    plt.close("all")


@pytest.fixture
def sample_df():
    """A small DataFrame useful across many tests."""
    return pd.DataFrame({
        "x": [1, 2, 3, 4, 5],
        "y": [2, 4, 1, 5, 3],
        "cat": ["a", "b", "a", "b", "a"],
        "size_col": [10, 20, 30, 40, 50],
        "series_a": [1, 4, 9, 16, 25],
        "series_b": [2, 3, 5, 7, 11],
    })


@pytest.fixture
def sample_dict():
    return {
        "x": [1, 2, 3],
        "y": [4, 5, 6],
        "cat": ["a", "b", "a"],
    }
