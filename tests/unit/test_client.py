"""Tests for mcp_garmin.client."""

from __future__ import annotations

import unittest.mock


from mcp_garmin.client import GarminClient, ToolError

# ---------------------------------------------------------------------------
# GarminClient constructor
# ---------------------------------------------------------------------------


def test_garmin_client_constructor():
    """Test GarminClient constructor with no injected client."""
    client = GarminClient()
    assert client._garth_client is None


def test_garmin_client_constructor_with_injected_client():
    """Test GarminClient constructor with injected client."""
    mock_client = unittest.mock.MagicMock()
    client = GarminClient(garth_client=mock_client)
    assert client._garth_client is mock_client


# ---------------------------------------------------------------------------
# GarminClient.get_client()
# ---------------------------------------------------------------------------


def test_garmin_client_get_client_with_injected_client():
    """Test GarminClient.get_client() with injected client."""
    mock_client = unittest.mock.MagicMock()
    client = GarminClient(garth_client=mock_client)

    result = client.get_client()

    assert result is mock_client


def test_garmin_client_get_client_no_injected_client():
    """Test GarminClient.get_client() without injected client."""
    # Mock the global _client to be None initially
    with unittest.mock.patch("mcp_garmin.client._client", None):
        # Just test that the method doesn't crash
        client = GarminClient()
        result = client.get_client()
        
        # Verify it returns some kind of client object
        assert result is not None
        # We can't easily mock the garth client due to how it's constructed,
        # but we can verify it doesn't crash


# ---------------------------------------------------------------------------
# GarminClient.get() and list()
# ---------------------------------------------------------------------------


def test_garmin_client_get():
    """Test GarminClient.get() method."""
    mock_client = unittest.mock.MagicMock()
    client = GarminClient(garth_client=mock_client)

    # Test with arguments
    result = client.get("/some/path", params={"key": "value"})

    mock_client.get.assert_called_once_with("/some/path", params={"key": "value"})
    assert result is mock_client.get.return_value


def test_garmin_client_list():
    """Test GarminClient.list() method."""
    mock_client = unittest.mock.MagicMock()
    client = GarminClient(garth_client=mock_client)

    # Test with arguments
    result = client.list("/some/path", params={"key": "value"})

    mock_client.list.assert_called_once_with("/some/path", params={"key": "value"})
    assert result is mock_client.list.return_value


# ---------------------------------------------------------------------------
# ToolError
# ---------------------------------------------------------------------------


def test_tool_error_is_exception():
    assert issubclass(ToolError, Exception)
