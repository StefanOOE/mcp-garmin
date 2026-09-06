"""Goal tools: steps goal, weight goal, Garmin fitness scores."""

from __future__ import annotations

from typing import Any

from .base import register
from ..garmin_service import GarminService


@register
def get_steps_goal(service: GarminService, day: str | None = None) -> dict[str, Any]:
    """Steps goal for a day (YYYY-MM-DD) — device + user + sync status."""
    return service.steps_goal(day=day)


@register
def get_weight_goal(service: GarminService, day: str | None = None) -> dict[str, Any]:
    """Weight goal for a day (YYYY-MM-DD) — target + target ranges."""
    return service.weight_goal(day=day)


@register
def get_garmin_scores(service: GarminService, day: str | None = None) -> dict[str, Any]:
    """Garmin fitness scores for a day (YYYY-MM-DD) — Vo2Max, Endurance, Power."""
    return service.garmin_scores(day=day)