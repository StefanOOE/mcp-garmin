"""Thin wrapper for hydration tools."""

from __future__ import annotations

from .base import register
from ..client import GarminClient


# Create a singleton client instance
_client_instance = GarminClient()


def get_client():
    """Get the Garmin client instance."""
    return _client_instance.get_client()


def _to_dict(obj):
    """Convert object to dict."""
    return _client_instance._to_dict(obj)


def _handle_garmin_error(func):
    """Handle Garmin errors."""
    return _client_instance._handle_garmin_error(func)


@register
@_handle_garmin_error
def get_daily_hydration(day: str | None = None) -> dict:
    """Daily hydration data for a day (YYYY-MM-DD)."""
    from garth.data import HydrationData
    client = get_client()
    result = HydrationData.get(day=day, client=client)
    return _to_dict(result)


@register
@_handle_garmin_error
def get_hydration_history(end: str | None = None, days: int = 7) -> list[dict]:
    """Hydration history for the last N days (up to end)."""
    from garth.data import HydrationData
    client = get_client()
    result = HydrationData.list(end=end, days=days, client=client)
    return [_to_dict(entry) for entry in result]