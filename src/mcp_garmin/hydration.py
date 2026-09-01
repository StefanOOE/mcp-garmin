"""Hydration-Tools: täglicher Flüssigkeitsstand und Verlauf."""
from __future__ import annotations

from .client import _handle_garmin_error, _to_dict, get_client


@_handle_garmin_error
def get_daily_hydration(day: str | None = None) -> dict:
    """Flüssigkeitsstand inkl. Tagesziel für einen Tag (YYYY-MM-DD)."""
    client = get_client()
    import garth

    result = garth.DailyHydration.all_data(day=day, client=client)
    return _to_dict(result)


@_handle_garmin_error
def get_hydration_history(end: str | None = None, days: int = 1) -> list[dict]:
    """Flüssigkeitsverlauf der letzten N Tage (period=days, bis end, YYYY-MM-DD)."""
    client = get_client()
    import garth

    result = garth.DailyHydration.list(end=end, period=days, client=client)
    return [_to_dict(entry) for entry in result]
