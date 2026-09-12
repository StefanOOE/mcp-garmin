"""Hydration tools: daily fluid intake and history.

Migrated to garth-ng 1.1.0 (S1 §1.6): ``garth.data.HydrationData`` does not
exist, so both tools use ``garth.DailyHydration.list`` (re-export of
``garth.stats.DailyHydration``) -- same contract as ``tools/hydration.py``
(no divergence). ``get_daily_hydration`` extracts the per-day entry
(``list(end=day, period=1)[0]``); history maps ``days`` → ``period``.
"""

from __future__ import annotations

from .client import _handle_garmin_error, _to_dict, get_client


@_handle_garmin_error
def get_daily_hydration(day: str | None = None) -> dict:
    """Fluid intake including daily goal for a day (YYYY-MM-DD)."""
    client = get_client()
    import garth

    result = garth.DailyHydration.list(end=day, period=1, client=client)
    if not result:
        return {}
    return _to_dict(result[0])


@_handle_garmin_error
def get_hydration_history(end: str | None = None, days: int = 1) -> list[dict]:
    """Fluid intake history for the last N days (period=days, up to end, YYYY-MM-DD)."""
    client = get_client()
    import garth

    result = garth.DailyHydration.list(end=end, period=days, client=client)
    return [_to_dict(entry) for entry in result]
