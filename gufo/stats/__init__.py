"""Statistical overlays and marks — requires scipy."""

try:
    import scipy  # noqa: F401
except ImportError:
    scipy = None


def _require_scipy(feature):
    """Raise ImportError with a helpful message if scipy is not installed."""
    if scipy is None:
        raise ImportError(
            f"{feature} requires scipy. Install it with: pip install gufo[scipy]"
        )
