"""Schlaf-Tools: Schlafstadien, Detaildaten, Tägliche Zusammenfassung (Schlafteil)."""
from __future__ import annotations

from typing import Any

from .client import _handle_garmin_error, _to_dict, get_client

# Felder in DailySummary, die schlafbezogen sind.
_SLEEP_FIELDS = (
    "sleeping_seconds",
    "sleep_time_seconds",
    "sleeping_seconds_from_sleep_sensor",
    "sleep_spo2_at_wake",
    "sleep_respiration_at_wake",
    "sleep_score",
    "sleep_start_timestamp_gmt",
    "sleep_end_timestamp_gmt",
    "sleep_start_timestamp_local",
    "sleep_end_timestamp_local",
    "sleep_maintenance_awakenings",
    "sleep_maintenance_awakening_duration_seconds",
    "sleep_time_from_sleep_sensor",
    "sleep_depth_seconds",
    "sleep_rem_seconds",
    "sleep_light_seconds",
    "sleep_awake_seconds",
    "sleep_unmeasurable_seconds",
    "sleep_maintenance_awakening_duration_seconds_from_sleep_sensor",
    "sleep_start_time_from_sleep_sensor",
    "sleep_start_time",
    "sleep_end_time",
    "sleep_duration_seconds",
)


@_handle_garmin_error
def get_sleep(day: str | None = None) -> dict:
    """Schlafdaten für einen Tag (YYYY-MM-DD) inkl. Schlafstadien-Zeiträume."""
    client = get_client()
    import garth

    result = garth.SleepData.get(day=day, client=client)
    return _to_dict(result)


@_handle_garmin_error
def get_sleep_detail(day: str | None = None) -> dict:
    """Schlaf-Details (Tagesdaten) für einen Tag (YYYY-MM-DD)."""
    client = get_client()
    from garth.data import DailySleepData

    result = DailySleepData.get(day=day, client=client)
    return _to_dict(result)


@_handle_garmin_error
def get_sleep_summary(day: str | None = None) -> dict:
    """Tägliche Zusammenfassung für einen Tag (YYYY-MM-DD).

    Liefert nur die schlafbezogenen Felder, sofern vorhanden, sonst das
    vollständige Dict.
    """
    client = get_client()
    from garth.data import DailySummary

    result = _to_dict(DailySummary.get(day=day, client=client))
    if isinstance(result, dict) and result:
        sleep_part: dict[str, Any] = {k: v for k, v in result.items() if k in _SLEEP_FIELDS}
        if sleep_part:
            return sleep_part
    return result
