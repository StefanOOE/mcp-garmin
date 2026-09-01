"""Device-Tools: Geräteinfo und Geräte-Liste."""
from __future__ import annotations

from .client import _handle_garmin_error, _to_dict, get_client


@_handle_garmin_error
def get_device_info() -> dict:
    """Aktives Garmin-Gerät: Typ, Name, Batteriestand."""
    client = get_client()
    import garth
    from garth.utils import camel_to_snake_dict

    # Try the deviceinfo endpoint; fall back to user profile
    try:
        raw = client.connectapi(
            '/connectapi/proxy/deviceinfo-service/device', method='GET'
        )
        return camel_to_snake_dict(raw) if raw else {}
    except Exception:
        # Fallback: extract from user profile
        profile = garth.UserProfile.get(client=client)
        result = _to_dict(profile)
        device_keys = {k: v for k, v in result.items() if 'device' in k.lower()}
        return device_keys if device_keys else result


@_handle_garmin_error
def get_connected_devices() -> list[dict]:
    """Liste aller verbundenen Garmin-Geräte."""
    client = get_client()
    import garth
    from garth.utils import camel_to_snake_dict

    try:
        raw = client.connectapi(
            '/connectapi/proxy/deviceinfo-service/devices', method='GET'
        )
        if isinstance(raw, list):
            return [camel_to_snake_dict(d) for d in raw]
        if isinstance(raw, dict):
            return [camel_to_snake_dict(raw)]
        return []
    except Exception:
        # Fallback: try user profile
        try:
            profile = garth.UserProfile.get(client=client)
            result = _to_dict(profile)
            devices = result.get('devices', result.get('connected_devices', []))
            if isinstance(devices, list):
                return devices
            return []
        except Exception:
            return []
