"""Util tools: user profile and user settings."""
from __future__ import annotations

from .client import _handle_garmin_error, _to_dict, get_client


@_handle_garmin_error
def get_user_profile() -> dict:
    """Garmin user profile: name, email, age, sex, height, location."""
    client = get_client()
    import garth

    result = garth.UserProfile.get(client=client)
    return _to_dict(result)


@_handle_garmin_error
def get_user_settings() -> dict:
    """User settings: VO2Max, thresholds, measurement system, sleep times."""
    client = get_client()
    import garth

    result = garth.UserSettings.get(client=client)
    return _to_dict(result)
