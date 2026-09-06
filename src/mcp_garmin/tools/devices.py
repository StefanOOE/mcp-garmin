"""Device tools: device info and device list."""

from __future__ import annotations

from typing import Any

from .base import register
from ..garmin_service import GarminService


@register
def get_device_info(service: GarminService) -> dict[str, Any]:
    """Active Garmin device: type, name, battery level."""
    return service.device_info()


@register
def get_connected_devices(service: GarminService) -> list[dict[str, Any]]:
    """List of all connected Garmin devices."""
    return service.connected_devices()