"""Activity tools: activity list, details, map, fitness activities, records."""

from __future__ import annotations

from typing import Any

from .base import register
from ..garmin_service import GarminService


@register
def get_activities(service: GarminService, limit: int = 20, start: int = 0) -> list[dict[str, Any]]:
    """List of recent activities (limit/start pagination)."""
    return service.activities(limit=limit, start=start)


@register
def get_activity_detail(service: GarminService, activity_id: int) -> dict[str, Any]:
    """Details for a single activity (activity_id)."""
    return service.activity_detail(activity_id=activity_id)


@register
def get_activity_map(service: GarminService, activity_id: int) -> dict[str, Any]:
    """Map data (GPS track) for an activity (activity_id)."""
    return service.activity_map(activity_id=activity_id)


@register
def get_fitness_activities(service: GarminService, end: str | None = None, days: int = 7) -> list[dict[str, Any]]:
    """Fitness activities (steps/calories) for the last N days (up to end)."""
    return service.fitness_activities(end=end, days=days)


@register
def get_personal_records(service: GarminService) -> list[dict[str, Any]]:
    """All personal records."""
    return service.personal_records()


@register
def get_personal_record_types(service: GarminService) -> list[dict[str, Any]]:
    """Available record types."""
    return service.personal_record_types()