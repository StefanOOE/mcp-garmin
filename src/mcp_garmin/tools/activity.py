"""Thin wrapper for activity tools.

Migrated to garth-ng 1.1.0 (S1 §1.1, concept §3.2) — same contract as
``mcp_garmin.activity`` (no divergence):

* ``get_activities`` -- ``garth.data.Activity.list(limit=..., start=...)``
  (**breaking**: ``end``/``days`` replaced by ``limit``/``start``).
* ``get_activity_detail`` -- ``garth.data.Activity.get(activity_id=...)``.
* ``get_activity_map`` -- Endpoint-Fallback ``client.connectapi(...)`` +
  ``camel_to_snake_dict()`` (no accessor in 1.1.0; payload keys
  ``activityHeatMapDTO`` + ``gPolyline``).
* ``get_fitness_activities`` -- ``garth.data.FitnessActivity.list(end=...,
  days=...)``.
* ``get_personal_records`` / ``get_personal_record_types`` -- Endpoint-Fallback
  (``/personalrecord-service/personalrecord[``+``type]``).

Endpoint paths carry **no** ``/connectapi``/``/proxy`` prefix --
``connectapi()`` builds the URL itself (S1 §0, live-verified Run #49).
"""

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
def get_activities(limit: int = 20, start: int = 0) -> list[dict]:
    """List of recent activities (limit/start pagination)."""
    from garth.data import Activity

    client = get_client()
    result = Activity.list(limit=limit, start=start, client=client)
    return [_to_dict(entry) for entry in result]


@register
@_handle_garmin_error
def get_activity_detail(activity_id: int) -> dict:
    """Details for a single activity (activity_id)."""
    from garth.data import Activity

    client = get_client()
    result = Activity.get(activity_id=activity_id, client=client)
    return _to_dict(result)


@register
@_handle_garmin_error
def get_activity_map(activity_id: int) -> dict:
    """Map data (GPS track) for an activity (activity_id).

    garth-ng 1.1.0 has no ``Activity.map_details`` accessor, so this uses the
    Endpoint-Fallback pattern: ``client.connectapi(path)`` +
    ``camel_to_snake_dict()`` (S1 §1.1, live-verified). The payload carries
    ``activityHeatMapDTO`` and ``gPolyline`` (camelCase → snake_case).
    """
    from garth.utils import camel_to_snake_dict

    client = get_client()
    raw = client.connectapi(f"/activity-service/activity/{activity_id}/mapdetails")
    return camel_to_snake_dict(raw) if raw else {}


@register
@_handle_garmin_error
def get_fitness_activities(end: str | None = None, days: int = 7) -> list[dict]:
    """Fitness activities (steps/calories) for the last N days (up to end)."""
    from garth.data import FitnessActivity

    client = get_client()
    result = FitnessActivity.list(end=end, days=days, client=client)
    return [_to_dict(entry) for entry in result]


@register
@_handle_garmin_error
def get_personal_records() -> list[dict]:
    """All personal records.

    garth-ng 1.1.0 has no personal-record accessor, so this uses the
    Endpoint-Fallback pattern (S1 §1.1, live-verified n=16).
    """
    from garth.utils import camel_to_snake_dict

    client = get_client()
    raw = client.connectapi("/personalrecord-service/personalrecord")
    return [camel_to_snake_dict(x) for x in raw] if raw else []


@register
@_handle_garmin_error
def get_personal_record_types() -> list[dict]:
    """Available record types.

    garth-ng 1.1.0 has no personal-record accessor, so this uses the
    Endpoint-Fallback pattern (S1 §1.1, live-verified n=51).
    """
    from garth.utils import camel_to_snake_dict

    client = get_client()
    raw = client.connectapi("/personalrecord-service/personalrecordtype")
    return [camel_to_snake_dict(x) for x in raw] if raw else []
