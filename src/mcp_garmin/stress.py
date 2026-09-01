"""Stress-Tools: Tages-/Wochen-Stress, Trainingsstatus, Morning Readiness."""
from __future__ import annotations

from .client import _handle_garmin_error, _to_dict, get_client


@_handle_garmin_error
def get_daily_stress(end: str | None = None, days: int = 1) -> list[dict]:
    """Stress-Verlauf der letzten N Tage (period=days, bis end, YYYY-MM-DD)."""
    client = get_client()
    import garth

    result = garth.DailyStress.list(end=end, period=days, client=client)
    return [_to_dict(entry) for entry in result]


@_handle_garmin_error
def get_weekly_stress(end: str | None = None) -> list[dict]:
    """Stress-Verlauf der letzten 7 Tage (bis end, YYYY-MM-DD)."""
    client = get_client()
    import garth

    result = garth.DailyStress.list(end=end, period=7, client=client)
    return [_to_dict(entry) for entry in result]


@_handle_garmin_error
def get_training_status_daily(day: str | None = None) -> list[dict]:
    """Trainingsstatus für einen Tag (YYYY-MM-DD)."""
    client = get_client()
    from garth.data import TrainingReadinessData

    result = TrainingReadinessData.get(day=day, client=client)
    if result is None:
        return []
    return [_to_dict(entry) for entry in result]


@_handle_garmin_error
def get_training_status_weekly(end: str | None = None) -> list[dict]:
    """Trainingsstatus der letzten Woche (bis end, YYYY-MM-DD)."""
    client = get_client()
    from garth.data import TrainingReadinessData

    result = TrainingReadinessData.get(day=end, client=client)
    if result is None:
        return []
    return [_to_dict(entry) for entry in result]


@_handle_garmin_error
def get_training_status_monthly(end: str | None = None) -> list[dict]:
    """Trainingsstatus des letzten Monats (bis end, YYYY-MM-DD)."""
    client = get_client()
    from garth.data import TrainingReadinessData

    result = TrainingReadinessData.get(day=end, client=client)
    if result is None:
        return []
    return [_to_dict(entry) for entry in result]


@_handle_garmin_error
def get_training_readiness(day: str | None = None) -> dict:
    """Morning Training Readiness für einen Tag (YYYY-MM-DD)."""
    client = get_client()
    from garth.data import MorningTrainingReadinessData

    result = MorningTrainingReadinessData.get(day=day, client=client)
    return _to_dict(result)


@_handle_garmin_error
def get_morning_readiness(day: str | None = None) -> dict:
    """Morning Readiness für einen Tag (YYYY-MM-DD) — Alias für get_training_readiness."""
    return get_training_readiness(day=day)
