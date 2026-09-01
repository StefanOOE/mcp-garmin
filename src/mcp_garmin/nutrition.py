"""Ernährungs-Tools: Ernährungs-Log und Ernährungs-Status."""
from __future__ import annotations

from .client import _handle_garmin_error, _to_dict, get_client


@_handle_garmin_error
def get_nutrition_log(day: str | None = None) -> dict:
    """Ernährungs-Log für einen Tag (YYYY-MM-DD) — Kalorien, Makros, Mahlzeiten."""
    client = get_client()
    from garth.data import NutritionLog

    result = NutritionLog.get(day=day, client=client)
    return _to_dict(result) if result is not None else {}


@_handle_garmin_error
def get_nutrition_status() -> dict:
    """Ernährungs-Status: aktuelle Kalorien-Ziele und Verbräuche."""
    client = get_client()
    from garth.data import NutritionStatus

    result = NutritionStatus.get(client=client)
    return _to_dict(result) if result is not None else {}
