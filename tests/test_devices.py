"""Tests für mcp_garmin.devices."""
from __future__ import annotations

from unittest.mock import patch


def _patch_client(monkeypatch, mock_client):
    import mcp_garmin.devices as devices

    monkeypatch.setattr(devices, "get_client", lambda: mock_client)


# --- get_device_info ---


def test_get_device_info_via_connectapi(monkeypatch, mock_client):
    """connectapi liefert ein Gerät → camelCase wird nach snake_case konvertiert."""
    import mcp_garmin.devices as devices

    fixture = {"deviceType": "watch", "deviceName": "Fenix 7", "batteryLevel": 80}
    mock_client.connectapi.return_value = fixture
    _patch_client(monkeypatch, mock_client)

    result = devices.get_device_info()

    mock_client.connectapi.assert_called_once()
    assert result == {"device_type": "watch", "device_name": "Fenix 7", "battery_level": 80}


def test_get_device_info_connectapi_empty(monkeypatch, mock_client):
    """connectapi liefert None/leeres → {} zurück."""
    import mcp_garmin.devices as devices

    mock_client.connectapi.return_value = None
    _patch_client(monkeypatch, mock_client)

    result = devices.get_device_info()

    assert result == {}


def test_get_device_info_fallback_to_profile(monkeypatch, mock_client):
    """connectapi wirft → Fallback auf UserProfile."""
    import mcp_garmin.devices as devices

    mock_client.connectapi.side_effect = Exception("404")
    profile = {"display_name": "SStrauss", "connected_device": "Fenix 7"}
    _patch_client(monkeypatch, mock_client)

    with patch("garth.UserProfile.get", return_value=profile):
        result = devices.get_device_info()

    # Nur device-bezogene Keys werden zurückgegeben
    assert result == {"connected_device": "Fenix 7"}


def test_get_device_info_fallback_no_device_keys(monkeypatch, mock_client):
    """connectapi wirft, Profil ohne device-Keys → gesamtes Profil zurück."""
    import mcp_garmin.devices as devices

    mock_client.connectapi.side_effect = Exception("404")
    profile = {"display_name": "SStrauss", "full_name": "Stefan"}
    _patch_client(monkeypatch, mock_client)

    with patch("garth.UserProfile.get", return_value=profile):
        result = devices.get_device_info()

    assert result == profile


# --- get_connected_devices ---


def test_get_connected_devices_via_connectapi(monkeypatch, mock_client):
    """connectapi liefert Liste → snake_case-Liste zurück."""
    import mcp_garmin.devices as devices

    fixture = [
        {"deviceType": "watch", "deviceName": "Fenix 7"},
        {"deviceType": "scale", "deviceName": "Index S2"},
    ]
    mock_client.connectapi.return_value = fixture
    _patch_client(monkeypatch, mock_client)

    result = devices.get_connected_devices()

    mock_client.connectapi.assert_called_once()
    assert result == [
        {"device_type": "watch", "device_name": "Fenix 7"},
        {"device_type": "scale", "device_name": "Index S2"},
    ]


def test_get_connected_devices_single_dict(monkeypatch, mock_client):
    """connectapi liefert ein einzelnes dict → in Liste gewrapped."""
    import mcp_garmin.devices as devices

    fixture = {"deviceType": "watch", "deviceName": "Fenix 7"}
    mock_client.connectapi.return_value = fixture
    _patch_client(monkeypatch, mock_client)

    result = devices.get_connected_devices()

    assert result == [{"device_type": "watch", "device_name": "Fenix 7"}]


def test_get_connected_devices_empty(monkeypatch, mock_client):
    """connectapi liefert None → [] zurück."""
    import mcp_garmin.devices as devices

    mock_client.connectapi.return_value = None
    _patch_client(monkeypatch, mock_client)

    result = devices.get_connected_devices()

    assert result == []


def test_get_connected_devices_fallback(monkeypatch, mock_client):
    """connectapi wirft → Fallback auf Profil; devices-Liste wird extrahiert."""
    import mcp_garmin.devices as devices

    mock_client.connectapi.side_effect = Exception("404")
    profile = {"display_name": "SStrauss", "devices": [{"name": "Fenix 7"}]}
    _patch_client(monkeypatch, mock_client)

    with patch("garth.UserProfile.get", return_value=profile):
        result = devices.get_connected_devices()

    assert result == [{"name": "Fenix 7"}]


def test_get_connected_devices_fallback_no_devices(monkeypatch, mock_client):
    """connectapi wirft, Profil ohne devices → [] zurück."""
    import mcp_garmin.devices as devices

    mock_client.connectapi.side_effect = Exception("404")
    profile = {"display_name": "SStrauss"}
    _patch_client(monkeypatch, mock_client)

    with patch("garth.UserProfile.get", return_value=profile):
        result = devices.get_connected_devices()

    assert result == []
