"""Tests for cerno.style — Theme, registry, palette."""
import matplotlib.pyplot as plt
import pytest

import cerno
from cerno.style.theme import (
    Theme, register_theme, get_theme, set_theme, theme_context,
    _resolve_theme, _PASSTHROUGH, _PassthroughTheme,
)
from cerno.style.color import Palette, CERNO_PALETTE


# ── Theme object ────────────────────────────────────────────────────

class TestTheme:
    def test_create_theme(self):
        t = Theme("test", {"axes.grid": True})
        assert t.name == "test"

    def test_theme_immutable_merge(self):
        t1 = Theme("base", {"axes.grid": True, "lines.linewidth": 1.0})
        t2 = t1.merge({"lines.linewidth": 3.0})
        # Original unchanged
        assert t1._rc["lines.linewidth"] == 1.0
        # New theme has override
        assert t2._rc["lines.linewidth"] == 3.0
        assert t2._rc["axes.grid"] is True

    def test_theme_rename(self):
        t = Theme("old", {"axes.grid": True})
        t2 = t.rename("new")
        assert t2.name == "new"
        assert t.name == "old"
        assert t2._rc == t._rc

    def test_as_context_scopes_rc(self):
        original = plt.rcParams["axes.grid"]
        t = Theme("ctx", {"axes.grid": not original})
        with t.as_context():
            assert plt.rcParams["axes.grid"] != original
        assert plt.rcParams["axes.grid"] == original


# ── Registry ────────────────────────────────────────────────────────

class TestRegistry:
    def test_builtin_themes_registered(self):
        for name in ("cerno_modern", "cerno_dark", "cerno_print"):
            theme = get_theme(name)
            assert isinstance(theme, Theme)
            assert theme.name == name

    def test_get_unknown_theme_raises(self):
        with pytest.raises(ValueError, match="Unknown theme"):
            get_theme("nonexistent_theme_xyz")

    def test_register_custom_theme(self):
        custom = Theme("my_custom", {"axes.grid": False})
        register_theme(custom)
        assert get_theme("my_custom") is custom

    def test_theme_context_manager(self):
        original = plt.rcParams.get("axes.facecolor")
        with theme_context("cerno_dark"):
            assert plt.rcParams["axes.facecolor"] == "#1e1e2e"
        assert plt.rcParams["axes.facecolor"] == original


# ── _resolve_theme ──────────────────────────────────────────────────

class TestResolveTheme:
    def test_none_returns_passthrough(self):
        result = _resolve_theme(None)
        assert isinstance(result, _PassthroughTheme)

    def test_string_resolves_to_theme(self):
        result = _resolve_theme("cerno_modern")
        assert isinstance(result, Theme)
        assert result.name == "cerno_modern"

    def test_theme_object_passthrough(self):
        t = Theme("direct", {})
        assert _resolve_theme(t) is t

    def test_invalid_type_raises(self):
        with pytest.raises(TypeError, match="theme name"):
            _resolve_theme(42)

    def test_passthrough_does_not_scope(self):
        """Passthrough theme should not wrap in rc_context."""
        before = dict(plt.rcParams)
        with _PASSTHROUGH.as_context():
            during = dict(plt.rcParams)
        assert before == during


# ── Palette ─────────────────────────────────────────────────────────

class TestPalette:
    def test_palette_has_categorical(self):
        assert len(CERNO_PALETTE.categorical) == 8

    def test_palette_has_sequential(self):
        assert len(CERNO_PALETTE.sequential) > 0

    def test_palette_has_diverging(self):
        assert len(CERNO_PALETTE.diverging) > 0

    def test_palette_colors_are_hex(self):
        for color in CERNO_PALETTE.categorical:
            assert color.startswith("#")
            assert len(color) == 7

    def test_theme_uses_palette_colors(self):
        """The modern theme's prop_cycle should reference the same palette."""
        theme = get_theme("cerno_modern")
        cycle_colors = [c["color"] for c in theme._rc["axes.prop_cycle"]]
        assert cycle_colors == CERNO_PALETTE.categorical


# ── Chart-level theme override ──────────────────────────────────────

class TestChartTheme:
    def test_chart_theme_by_name(self, sample_df, tmp_path):
        (cerno.chart(sample_df)
         .scatter("x", "y")
         .theme("cerno_dark")
         .save(tmp_path / "dark.png"))

    def test_chart_theme_by_object(self, sample_df, tmp_path):
        custom = Theme("inline", {"axes.facecolor": "#ff0000"})
        (cerno.chart(sample_df)
         .scatter("x", "y")
         .theme(custom)
         .save(tmp_path / "custom.png"))
