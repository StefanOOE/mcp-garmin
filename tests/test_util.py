"""Tests for util.py."""
from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest


@pytest.fixture
def mock_client(monkeypatch):
    """Patches get_client to return a MagicMock."""
    client = MagicMock()
    monkeypatch.setattr("mcp_garmin.client._client", client)
    return client


class TestUserProfile:
    def test_returns_dict(self, mock_client):
        from mcp_garmin.util import get_user_profile

        expected = {"userName": "hmpftata", "email": "test@example.com"}
        with patch("garth.UserProfile.get", return_value=MagicMock()):
            with patch("mcp_garmin.client.asdict", return_value=expected):
                result = get_user_profile()
                assert result == expected

    def test_handles_none(self, mock_client):
        from mcp_garmin.util import get_user_profile

        with patch("garth.UserProfile.get", return_value=None):
            result = get_user_profile()
            assert result == {}


class TestUserSettings:
    def test_returns_dict(self, mock_client):
        from mcp_garmin.util import get_user_settings

        expected = {"id": 1, "user_data": {"height": 180.0}}
        with patch("garth.UserSettings.get", return_value=MagicMock()):
            with patch("mcp_garmin.client.asdict", return_value=expected):
                result = get_user_settings()
                assert result == expected
