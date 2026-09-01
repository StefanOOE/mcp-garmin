"""Tests für mcp_garmin.client."""
from __future__ import annotations

import unittest.mock

import pytest
from garth import http as garth_http
from garth.exc import GarthException

from mcp_garmin import client
from mcp_garmin.client import ToolError, _handle_garmin_error, _to_dict, get_client

# ---------------------------------------------------------------------------
# get_client()
# ---------------------------------------------------------------------------


def test_get_client_returns_client(monkeypatch):
    """get_client() liefert den (mockten) garth Client mit konfiguriertem Storage."""
    mock_client = unittest.mock.MagicMock()
    mock_storage_instance = unittest.mock.MagicMock()
    mock_storage_cls = unittest.mock.MagicMock(return_value=mock_storage_instance)
    mock_storage_instance.load.return_value = "token"

    monkeypatch.setattr(client, "_client", None)
    monkeypatch.setattr(garth_http, "client", mock_client)
    monkeypatch.setattr(client, "FileTokenStorage", mock_storage_cls)

    result = get_client()

    assert result is mock_client
    assert mock_client.storage is mock_storage_instance
    assert mock_client.oauth2_token == "token"
    mock_storage_cls.assert_called_once()
    mock_storage_instance.load.assert_called_once()


def test_get_client_caches(monkeypatch):
    """Gecachter Client wird wiederverwendet (zweiter Aufruf liefert denselben)."""
    sentinel = object()
    monkeypatch.setattr(client, "_client", sentinel)
    assert get_client() is sentinel


# ---------------------------------------------------------------------------
# ToolError
# ---------------------------------------------------------------------------


def test_tool_error_is_exception():
    assert issubclass(ToolError, Exception)


# ---------------------------------------------------------------------------
# _to_dict()
# ---------------------------------------------------------------------------


def test_to_dict_none():
    assert _to_dict(None) == {}


def test_to_dict_passthrough():
    d = {"a": 1}
    assert _to_dict(d) is d


def test_to_dict_asdict():
    obj = object()
    with unittest.mock.patch.object(client, "asdict", return_value={"b": 2}) as mock_asdict:
        result = _to_dict(obj)
    mock_asdict.assert_called_once_with(obj)
    assert result == {"b": 2}


# ---------------------------------------------------------------------------
# _handle_garmin_error()
# ---------------------------------------------------------------------------


def test_handle_garmin_error_token_hint():
    """GarthException mit 'token' im Text → ToolError mit garmin_login.py-Hint."""

    def broken() -> None:
        raise GarthException("Invalid token for user")

    wrapped = _handle_garmin_error(broken)
    with pytest.raises(ToolError) as excinfo:
        wrapped()
    assert "garmin_login.py" in str(excinfo.value)
    assert "Invalid token for user" in str(excinfo.value)


def test_handle_garmin_error_non_token():
    """GarthException ohne 'token' → ToolError ohne garmin_login.py-Hint."""

    def broken() -> None:
        raise GarthException("Connection timeout")

    wrapped = _handle_garmin_error(broken)
    with pytest.raises(ToolError) as excinfo:
        wrapped()
    assert "garmin_login.py" not in str(excinfo.value)
    assert "Connection timeout" in str(excinfo.value)


def test_handle_garmin_error_non_garth_exception_passes_through():
    """Nicht-Garth-Exceptionen (z.B. ValueError) werden unverändert weitergeworfen."""

    def broken() -> None:
        raise ValueError("boom")

    wrapped = _handle_garmin_error(broken)
    with pytest.raises(ValueError, match="boom"):
        wrapped()
