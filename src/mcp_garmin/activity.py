"""Aktivitäts-Tools: Aktivitätsliste, Details, Karte, Fitness-Aktivitäten, Rekorde."""
from __future__ import annotations

from .client import _handle_garmin_error, _to_dict, get_client


@_handle_garmin_error
def get_activities(limit: int = 20, start: int = 0) -> list[dict]:
    """Liste der letzten Aktivitäten (limit/start-Pagination)."""
    client = get_client()
    from garth.data import Activity

    result = Activity.list(limit=limit, start=start, client=client)
    return [_to_dict(entry) for entry in result]


@_handle_garmin_error
def get_activity_detail(activity_id: int) -> dict:
    """Details zu einer einzelnen Aktivität (activity_id)."""
    client = get_client()
    from garth.data import Activity

    result = Activity.get(activity_id=activity_id, client=client)
    return _to_dict(result)


@_handle_garmin_error
def get_activity_map(activity_id: int) -> dict:
    """Kartendaten (GPS-Track) zu einer Aktivität (activity_id)."""
    client = get_client()
    from garth.data import Activity

    result = Activity.map_details(activity_id=activity_id, client=client)
    return _to_dict(result)


@_handle_garmin_error
def get_fitness_activities(end: str | None = None, days: int = 7) -> list[dict]:
    """Fitness-Aktivitäten (Schritte/Kalorien) der letzten N Tage (bis end)."""
    client = get_client()
    from garth.data import FitnessActivity

    result = FitnessActivity.list(end=end, days=days, client=client)
    return [_to_dict(entry) for entry in result]


@_handle_garmin_error
def get_personal_records() -> list[dict]:
    """Alle persönlichen Rekorde."""
    client = get_client()
    from garth.data import PersonalRecord

    result = PersonalRecord.list(client=client)
    return [_to_dict(entry) for entry in result]


@_handle_garmin_error
def get_personal_record_types() -> list[dict]:
    """Verfügbare Rekorde-Typen."""
    client = get_client()
    from garth.data import PersonalRecordType

    result = PersonalRecordType.list(client=client)
    return [_to_dict(entry) for entry in result]
