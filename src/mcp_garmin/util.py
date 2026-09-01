"""Util-Tools: Benutzerprofil und Benutzer-Einstellungen."""
from __future__ import annotations

from .client import _handle_garmin_error, _to_dict, get_client


@_handle_garmin_error
def get_user_profile() -> dict:
    """Garmin-Benutzerprofil: Name, E-Mail, Alter, Geschlecht, Körpergröße, Standort."""
    client = get_client()
    import garth

    result = garth.UserProfile.get(client=client)
    return _to_dict(result)


@_handle_garmin_error
def get_user_settings() -> dict:
    """Benutzer-Einstellungen: VO2Max, Schwellenwerte, Messsystem, Schlafzeiten."""
    client = get_client()
    import garth

    result = garth.UserSettings.get(client=client)
    return _to_dict(result)
