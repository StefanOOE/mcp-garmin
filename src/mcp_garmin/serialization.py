"""Serialization helpers for Garmin data."""

from __future__ import annotations

from typing import Any


def camel_to_snake_dict(data: dict[str, Any]) -> dict[str, Any]:
    """Convert a dictionary with camelCase keys to snake_case keys."""
    # Import here to avoid circular import issues
    from garth.utils import camel_to_snake_dict as _camel_to_snake_dict

    return _camel_to_snake_dict(data)


# Fields in DailySummary that are sleep-related.
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


def project_sleep_fields(data: dict[str, Any]) -> dict[str, Any]:
    """Project only sleep-related fields from a DailySummary."""
    if not data:
        return {}
    return {k: v for k, v in data.items() if k in _SLEEP_FIELDS}
