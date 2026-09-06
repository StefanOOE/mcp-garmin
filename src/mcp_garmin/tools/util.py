"""Util tools: user profile and user settings."""

from __future__ import annotations

from typing import Any

from .base import register
from ..garmin_service import GarminService


@register
def get_user_profile(service: GarminService) -> dict[str, Any]:
    """Garmin user profile: name, email, age, sex, height, location."""
    return service.user_profile()


@register
def get_user_settings(service: GarminService) -> dict[str, Any]:
    """User settings: VO2Max, thresholds, measurement system, sleep times."""
    return service.user_settings()