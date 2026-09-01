"""Schritt-Tools: Tages-/Wochen-Schritte, tägliche Zusammenfassung."""
from __future__ import annotations

from .client import _handle_garmin_error, _to_dict, get_client


@_handle_garmin_error
def get_daily_steps(end: str | None = None) -> list[dict]:
    """Schrittzahl der letzten 1 Tage (period=1, bis end, YYYY-MM-DD)."""
    client = get_client()
    import garth

    result = garth.DailySteps.list(end=end, period=1, client=client)
    return [_to_dict(entry) for entry in result]


@_handle_garmin_error
def get_weekly_steps(end: str | None = None) -> list[dict]:
    """Schrittzahl der letzten 7 Tage (period=7, bis end, YYYY-MM-DD)."""
    client = get_client()
    import garth

    result = garth.DailySteps.list(end=end, period=7, client=client)
    return [_to_dict(entry) for entry in result]


@_handle_garmin_error
def get_daily_summary(day: str | None = None) -> dict:
    """Tägliche Zusammenfassung für einen Tag (YYYY-MM-DD): Schritte, Kalorien, Herzfrequenz."""
    client = get_client()
    from garth.data import DailySummary

    result = DailySummary.get(day=day, client=client)
    return _to_dict(result)


@_handle_garmin_error
def get_daily_summary_history(end: str | None = None, days: int = 7) -> list[dict]:
    """Tägliche Zusammenfassung der letzten N Tage (bis end, YYYY-MM-DD)."""
    client = get_client()
    from garth.data import DailySummary

    result = DailySummary.list(end=end, days=days, client=client)
    return [_to_dict(entry) for entry in result]
