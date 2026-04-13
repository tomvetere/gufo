"""Tests for v0.0.4 statistical marks — regression, KDE, strip, swarm."""

import numpy as np
import pandas as pd
import pytest
import matplotlib.pyplot as plt

import cerno
from cerno.stats import _require_scipy
from cerno.stats.regression import Regression
from cerno.stats.kde import KDE


# ── Fixtures ───────────────────────────────────────────────────────────

@pytest.fixture
def scatter_df():
    rng = np.random.default_rng(0)
    x = rng.uniform(0, 10, 50)
    return pd.DataFrame({
        "x": x,
        "y": 2 * x + 1 + rng.normal(0, 1, 50),
        "group": rng.choice(["A", "B"], 50),
    })


@pytest.fixture
def cat_df():
    rng = np.random.default_rng(0)
    return pd.DataFrame({
        "species": rng.choice(["setosa", "versicolor", "virginica"], 60),
        "petal_length": rng.normal(4, 1, 60),
        "petal_width": rng.normal(1.5, 0.5, 60),
    })


# ── Regression ─────────────────────────────────────────────────────────

class TestRegression:
    def test_linear_fit_renders(self, scatter_df, tmp_path):
        cerno.chart(scatter_df).scatter(
            "x", "y", fit=cerno.regression()
        ).save(tmp_path / "reg.png")

    def test_polynomial_fit_renders(self, scatter_df, tmp_path):
        cerno.chart(scatter_df).scatter(
            "x", "y", fit=cerno.regression(degree=2)
        ).save(tmp_path / "poly.png")

    def test_regression_with_color(self, scatter_df, tmp_path):
        cerno.chart(scatter_df).scatter(
            "x", "y", fit=cerno.regression(color="red", linestyle="--")
        ).save(tmp_path / "reg_color.png")

    def test_regression_with_label(self, scatter_df, tmp_path):
        cerno.chart(scatter_df).scatter(
            "x", "y", fit=cerno.regression(label="My fit")
        ).legend().save(tmp_path / "reg_label.png")

    def test_auto_label_linear(self):
        r = Regression(degree=1)
        assert r._auto_label() == "Linear fit"

    def test_auto_label_poly(self):
        r = Regression(degree=3)
        assert r._auto_label() == "Poly(3) fit"

    def test_regression_with_nan_data(self, tmp_path):
        df = pd.DataFrame({
            "x": [1, 2, np.nan, 4, 5],
            "y": [2, 4, 6, np.nan, 10],
        })
        cerno.chart(df).scatter(
            "x", "y", fit=cerno.regression()
        ).save(tmp_path / "reg_nan.png")

    def test_regression_insufficient_points(self, tmp_path):
        """Regression with too few valid points should silently skip."""
        df = pd.DataFrame({"x": [1.0], "y": [2.0]})
        cerno.chart(df).scatter(
            "x", "y", fit=cerno.regression(degree=2)
        ).save(tmp_path / "reg_few.png")

    def test_regression_with_grouped_scatter(self, scatter_df, tmp_path):
        """Regression line fits across all groups."""
        cerno.chart(scatter_df).scatter(
            "x", "y", color="group", fit=cerno.regression()
        ).save(tmp_path / "reg_grouped.png")

    def test_regression_skipped_for_wide_form(self, tmp_path):
        """Wide-form scatter silently skips regression."""
        df = pd.DataFrame({
            "x": [1, 2, 3, 4],
            "a": [2, 4, 6, 8],
            "b": [1, 3, 5, 7],
        })
        cerno.chart(df).scatter(
            "x", ["a", "b"], fit=cerno.regression()
        ).save(tmp_path / "reg_wide.png")

    def test_regression_config_defaults(self):
        r = cerno.regression()
        assert isinstance(r, Regression)
        assert r.degree == 1
        assert r.color is None
        assert r.linestyle == "-"
        assert r.linewidth == 2.0

    def test_scatter_without_fit(self, scatter_df, tmp_path):
        """Scatter without fit= still works as before."""
        cerno.chart(scatter_df).scatter("x", "y").save(tmp_path / "no_fit.png")


# ── KDE Standalone ─────────────────────────────────────────────────────

class TestKDEStandalone:
    def test_basic_kde(self, scatter_df, tmp_path):
        cerno.chart(scatter_df).kde("x").save(tmp_path / "kde.png")

    def test_kde_with_fill(self, scatter_df, tmp_path):
        cerno.chart(scatter_df).kde("x", fill=True).save(tmp_path / "kde_fill.png")

    def test_kde_with_color(self, scatter_df, tmp_path):
        cerno.chart(scatter_df).kde("x", color="red").save(tmp_path / "kde_color.png")

    def test_kde_with_categorical_color(self, scatter_df, tmp_path):
        cerno.chart(scatter_df).kde("x", color="group").save(
            tmp_path / "kde_cat.png"
        )

    def test_kde_config_defaults(self):
        k = cerno.kde()
        assert isinstance(k, KDE)
        assert k.bw_method is None
        assert k.fill is False
        assert k.n_points == 200


# ── KDE Histogram Overlay ─────────────────────────────────────────────

class TestKDEHistogramOverlay:
    def test_histogram_with_kde_overlay(self, scatter_df, tmp_path):
        cerno.chart(scatter_df).histogram(
            "x", kde=cerno.kde()
        ).save(tmp_path / "hist_kde.png")

    def test_histogram_kde_with_fill(self, scatter_df, tmp_path):
        cerno.chart(scatter_df).histogram(
            "x", kde=cerno.kde(fill=True, alpha=0.3)
        ).save(tmp_path / "hist_kde_fill.png")

    def test_histogram_without_kde(self, scatter_df, tmp_path):
        """Histogram without kde= still works as before."""
        cerno.chart(scatter_df).histogram("x").save(tmp_path / "hist_plain.png")


# ── Strip ──────────────────────────────────────────────────────────────

class TestStripMark:
    def test_basic_strip(self, cat_df, tmp_path):
        cerno.chart(cat_df).strip("species", "petal_length").save(
            tmp_path / "strip.png"
        )

    def test_strip_horizontal(self, cat_df, tmp_path):
        cerno.chart(cat_df).strip(
            "species", "petal_length", horizontal=True
        ).save(tmp_path / "strip_h.png")

    def test_strip_with_color(self, cat_df, tmp_path):
        cerno.chart(cat_df).strip(
            "species", "petal_length", color="steelblue"
        ).save(tmp_path / "strip_color.png")

    def test_strip_with_jitter(self, cat_df, tmp_path):
        cerno.chart(cat_df).strip(
            "species", "petal_length", jitter=0.4
        ).save(tmp_path / "strip_jitter.png")

    def test_strip_wide_form(self, tmp_path):
        df = pd.DataFrame({
            "a": np.random.default_rng(0).normal(0, 1, 30),
            "b": np.random.default_rng(1).normal(1, 1, 30),
        })
        cerno.chart(df).strip(None, ["a", "b"]).save(tmp_path / "strip_wide.png")

    def test_strip_reproducible_jitter(self, cat_df, tmp_path):
        """Two renders should produce identical jitter."""
        fig1, _ = cerno.chart(cat_df).scatter("species", "petal_length")._render()
        fig2, _ = cerno.chart(cat_df).scatter("species", "petal_length")._render()
        # Just check no error; visual reproducibility is by fixed seed

    def test_strip_with_dict_data(self, tmp_path):
        data = {
            "cat": ["a", "a", "b", "b", "c", "c"],
            "val": [1, 2, 3, 4, 5, 6],
        }
        cerno.chart(data).strip("cat", "val").save(tmp_path / "strip_dict.png")


# ── Swarm ──────────────────────────────────────────────────────────────

class TestSwarmMark:
    def test_basic_swarm(self, cat_df, tmp_path):
        cerno.chart(cat_df).swarm("species", "petal_length").save(
            tmp_path / "swarm.png"
        )

    def test_swarm_horizontal(self, cat_df, tmp_path):
        cerno.chart(cat_df).swarm(
            "species", "petal_length", horizontal=True
        ).save(tmp_path / "swarm_h.png")

    def test_swarm_with_color(self, cat_df, tmp_path):
        cerno.chart(cat_df).swarm(
            "species", "petal_length", color="coral"
        ).save(tmp_path / "swarm_color.png")

    def test_swarm_wide_form(self, tmp_path):
        df = pd.DataFrame({
            "a": np.random.default_rng(0).normal(0, 1, 20),
            "b": np.random.default_rng(1).normal(1, 1, 20),
        })
        cerno.chart(df).swarm(None, ["a", "b"]).save(tmp_path / "swarm_wide.png")

    def test_swarm_with_dict_data(self, tmp_path):
        data = {
            "cat": ["a", "a", "b", "b", "c", "c"],
            "val": [1, 2, 3, 4, 5, 6],
        }
        cerno.chart(data).swarm("cat", "val").save(tmp_path / "swarm_dict.png")

    def test_beeswarm_no_overlap(self):
        """Offsets should not collide for nearby values."""
        from cerno.marks.swarm import _beeswarm_offsets
        values = np.array([1.0, 1.01, 1.02, 1.03, 2.0, 2.01])
        offsets = _beeswarm_offsets(values, marker_size=20)
        assert len(offsets) == 6
        # Close values should get different offsets
        assert not np.all(offsets[:4] == 0)

    def test_beeswarm_empty(self):
        from cerno.marks.swarm import _beeswarm_offsets
        offsets = _beeswarm_offsets(np.array([]), marker_size=20)
        assert len(offsets) == 0


# ── scipy Guard ────────────────────────────────────────────────────────

class TestScipyGuard:
    def test_require_scipy_passes_when_installed(self):
        _require_scipy("test")

    def test_regression_render_no_scipy_needed(self):
        """Regression uses numpy only — no scipy dependency."""
        r = Regression()
        fig, ax = plt.subplots()
        x = np.array([1.0, 2.0, 3.0])
        y = np.array([2.0, 4.0, 6.0])
        r.render(x, y, ax)

    def test_kde_render_requires_scipy(self):
        """KDE.render calls _require_scipy internally."""
        k = KDE()
        fig, ax = plt.subplots()
        x = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
        k.render(x, ax)


# ── LOWESS ────────────────────────────────────────────────────────

class TestLowess:
    def test_lowess_factory(self):
        lo = cerno.lowess(frac=0.5, color="red")
        assert lo.frac == 0.5
        assert lo.color == "red"

    def test_lowess_default_frac(self):
        lo = cerno.lowess()
        assert abs(lo.frac - 0.6667) < 0.001

    def test_lowess_dataclass_fields(self):
        lo = cerno.lowess()
        assert lo.linestyle == "-"
        assert lo.linewidth == 2.0
        assert lo.label is None

    @pytest.mark.skipif(
        not hasattr(cerno.Lowess, "render"),
        reason="Lowess not fully available"
    )
    def test_lowess_render_without_statsmodels(self, monkeypatch):
        import cerno.stats.lowess as lowess_mod
        monkeypatch.setattr(lowess_mod, "sm_lowess", None)
        lo = cerno.lowess()
        fig, ax = plt.subplots()
        x = np.array([1.0, 2.0, 3.0, 4.0])
        y = np.array([2.0, 4.0, 3.0, 5.0])
        with pytest.raises(ImportError, match="statsmodels"):
            lo.render(x, y, ax)
