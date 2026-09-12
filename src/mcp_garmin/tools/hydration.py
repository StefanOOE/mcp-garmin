"""Thin wrapper for hydration tools.

garth-ng 1.1.0 has no ``garth.data.HydrationData`` accessor, so both tools use
``garth.stats.DailyHydration.list`` (S1 §1.6, concept §3.2):

* ``get_daily_hydration`` -- Remap ``data→stats``, ``.get→.list``:
  ``list(end=day, period=1)`` + extract the per-day entry (``[0]``).
* ``get_hydration_history`` -- ``list(end=end, period=days)``
  (``days→period``).
"""

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
    from garth.stats import DailyHydration

    client = get_client()
    result = DailyHydration.list(end=day, period=1, client=client)
    if not result:
        return {}
    return _to_dict(result[0])


@register
@_handle_garmin_error
def get_hydration_history(end: str | None = None, days: int = 7) -> list[dict]:
    """Hydration history for the last N days (up to end)."""
    from garth.stats import DailyHydration

    client = get_client()
    result = DailyHydration.list(end=end, period=days, client=client)
    return [_to_dict(entry) for entry in result]
