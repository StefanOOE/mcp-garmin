"""Activity tools: activity list, details, map, fitness activities, records."""
from __future__ import annotations

from .client import _handle_garmin_error, _to_dict, get_client


@_handle_garmin_error
def get_activities(limit: int = 20, start: int = 0) -> list[dict]:
    """List of recent activities (limit/start pagination)."""
    client = get_client()
    from garth.data import Activity

    result = Activity.list(limit=limit, start=start, client=client)
    return [_to_dict(entry) for entry in result]


@_handle_garmin_error
def get_activity_detail(activity_id: int) -> dict:
    """Details for a single activity (activity_id)."""
    client = get_client()
    from garth.data import Activity

    result = Activity.get(activity_id=activity_id, client=client)
    return _to_dict(result)


@_handle_garmin_error
def get_activity_map(activity_id: int) -> dict:
    """Map data (GPS track) for an activity (activity_id)."""
    client = get_client()
    from garth.data import Activity

    result = Activity.map_details(activity_id=activity_id, client=client)
    return _to_dict(result)


@_handle_garmin_error
def get_fitness_activities(end: str | None = None, days: int = 7) -> list[dict]:
    """Fitness activities (steps/calories) for the last N days (up to end)."""
    client = get_client()
    from garth.data import FitnessActivity

    result = FitnessActivity.list(end=end, days=days, client=client)
    return [_to_dict(entry) for entry in result]


@_handle_garmin_error
def get_personal_records() -> list[dict]:
    """All personal records."""
    client = get_client()
    from garth.data import PersonalRecord

    result = PersonalRecord.list(client=client)
    return [_to_dict(entry) for entry in result]


@_handle_garmin_error
def get_personal_record_types() -> list[dict]:
    """Available record types."""
    client = get_client()
    from garth.data import PersonalRecordType

    result = PersonalRecordType.list(client=client)
    return [_to_dict(entry) for entry in result]
