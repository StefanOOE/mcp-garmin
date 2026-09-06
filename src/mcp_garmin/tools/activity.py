"""Thin wrapper for activity tools."""

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
def get_activities(end: str | None = None, days: int = 7) -> list[dict]:
    """Activities list for the last N days (up to end)."""
    from garth.data import Activities

    client = get_client()
    result = Activities.list(end=end, days=days, client=client)
    return [_to_dict(entry) for entry in result]


@register
@_handle_garmin_error
def get_activity_detail(activity_id: str) -> dict:
    """Activity detail for a specific activity ID."""
    from garth.data import ActivityDetail

    client = get_client()
    result = ActivityDetail.get(activity_id=activity_id, client=client)
    return _to_dict(result)


@register
@_handle_garmin_error
def get_activity_map(activity_id: str) -> dict:
    """Activity map for a specific activity ID."""
    from garth.data import ActivityMap

    client = get_client()
    result = ActivityMap.get(activity_id=activity_id, client=client)
    return _to_dict(result)


@register
@_handle_garmin_error
def get_fitness_activities(end: str | None = None, days: int = 7) -> list[dict]:
    """Fitness activities list for the last N days (up to end)."""
    from garth.data import FitnessActivities

    client = get_client()
    result = FitnessActivities.list(end=end, days=days, client=client)
    return [_to_dict(entry) for entry in result]


@register
@_handle_garmin_error
def get_personal_records() -> list[dict]:
    """Personal records."""
    from garth.data import PersonalRecords

    client = get_client()
    result = PersonalRecords.get(client=client)
    return [_to_dict(entry) for entry in result]


@register
@_handle_garmin_error
def get_personal_record_types() -> list[dict]:
    """Personal record types."""
    from garth.data import PersonalRecordTypes

    client = get_client()
    result = PersonalRecordTypes.get(client=client)
    return [_to_dict(entry) for entry in result]
