"""Unit tests for util tools."""
from __future__ import annotations

from unittest.mock import MagicMock, patch

from mcp_garmin.tools.util import get_user_profile, get_user_settings


def test_get_user_profile():
    """User profile."""
    expected = {"userName": "hmpftata", "email": "test@example.com"}
    mock_client = MagicMock()
    
    with patch("garth.users.UserProfile.get", return_value=MagicMock()):
        with patch("mcp_garmin.client.asdict", return_value=expected):
            result = get_user_profile()
            assert result == expected


def test_get_user_profile_none():
    """User profile handles None return."""
    mock_client = MagicMock()
    
    with patch("garth.users.UserProfile.get", return_value=None):
        result = get_user_profile()
        assert result == {}


def test_get_user_settings():
    """User settings."""
    expected = {"id": 1, "user_data": {"height": 180.0}}
    mock_client = MagicMock()
    
    with patch("garth.users.UserSettings.get", return_value=MagicMock()):
        with patch("mcp_garmin.client.asdict", return_value=expected):
            result = get_user_settings()
            assert result == expected