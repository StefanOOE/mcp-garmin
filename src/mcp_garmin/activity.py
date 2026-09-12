"""Activity tools: activity list, details, map, fitness activities, records.

Migrated to garth-ng 1.1.0 (S1 §1.1, concept §3.2):

* ``get_activities`` -- ``garth.data.Activity.list(limit=..., start=...)``
  (**breaking**: ``end``/``days`` replaced by ``limit``/``start`` pagination).
* ``get_activity_detail`` -- ``garth.data.Activity.get(activity_id=...)``
  (class rename ``ActivityDetail`` → ``Activity``).
* ``get_activity_map`` -- **no accessor** (``Activity.map_details`` does not
  exist in 1.1.0) → Endpoint-Fallback ``client.connectapi(...)`` +
  ``camel_to_snake_dict()`` (live payload: ``activityHeatMapDTO`` +
  ``gPolyline``, both fields).
* ``get_fitness_activities`` -- ``garth.data.FitnessActivity.list(end=...,
  days=...)`` (class rename ``FitnessActivities`` → ``FitnessActivity``).
* ``get_personal_records`` / ``get_personal_record_types`` -- **no accessor**
  → Endpoint-Fallback (``/personalrecord-service/personalrecord`` /
  ``/personalrecord-service/personalrecordtype``).

Endpoint paths carry **no** ``/connectapi``/``/proxy`` prefix --
``connectapi()`` builds the URL itself (S1 §0, live-verified Run #49).
"""

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
    """Map data (GPS track) for an activity (activity_id).

    garth-ng 1.1.0 has no ``Activity.map_details`` accessor, so this uses the
    Endpoint-Fallback pattern: ``client.connectapi(path)`` +
    ``camel_to_snake_dict()`` (S1 §1.1, live-verified). The payload carries
    ``activityHeatMapDTO`` and ``gPolyline`` (camelCase → snake_case).
    """
    client = get_client()
    from garth.utils import camel_to_snake_dict

    raw = client.connectapi(f"/activity-service/activity/{activity_id}/mapdetails")
    return camel_to_snake_dict(raw) if raw else {}


@_handle_garmin_error
def get_fitness_activities(end: str | None = None, days: int = 7) -> list[dict]:
    """Fitness activities (steps/calories) for the last N days (up to end)."""
    client = get_client()
    from garth.data import FitnessActivity

    result = FitnessActivity.list(end=end, days=days, client=client)
    return [_to_dict(entry) for entry in result]


@_handle_garmin_error
def get_personal_records() -> list[dict]:
    """All personal records.

    garth-ng 1.1.0 has no personal-record accessor, so this uses the
    Endpoint-Fallback pattern (S1 §1.1, live-verified n=16).
    """
    client = get_client()
    from garth.utils import camel_to_snake_dict

    raw = client.connectapi("/personalrecord-service/personalrecord")
    return [camel_to_snake_dict(x) for x in raw] if raw else []


@_handle_garmin_error
def get_personal_record_types() -> list[dict]:
    """Available record types.

    garth-ng 1.1.0 has no personal-record accessor, so this uses the
    Endpoint-Fallback pattern (S1 §1.1, live-verified n=51).
    """
    client = get_client()
    from garth.utils import camel_to_snake_dict

    raw = client.connectapi("/personalrecord-service/personalrecordtype")
    return [camel_to_snake_dict(x) for x in raw] if raw else []
