"""Thin wrapper for devices tools."""

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
def get_connected_devices() -> list[dict]:
    """Connected devices."""
    from garth.data import ConnectedDevices

    client = get_client()
    result = ConnectedDevices.get(client=client)
    return [_to_dict(entry) for entry in result]


@register
@_handle_garmin_error
def get_device_info(device_id: str) -> dict:
    """Device info for a specific device ID."""
    from garth.data import DeviceInfo

    client = get_client()
    result = DeviceInfo.get(device_id=device_id, client=client)
    return _to_dict(result)
