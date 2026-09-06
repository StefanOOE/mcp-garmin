"""Thin wrapper for util tools."""

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
def get_user_profile() -> dict:
    """User profile."""
    from garth.data import UserProfile

    client = get_client()
    result = UserProfile.get(client=client)
    return _to_dict(result)


@register
@_handle_garmin_error
def get_user_settings() -> dict:
    """User settings."""
    from garth.data import UserSettings

    client = get_client()
    result = UserSettings.get(client=client)
    return _to_dict(result)
