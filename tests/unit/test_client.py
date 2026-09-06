"""Tests for mcp_garmin.client."""

from __future__ import annotations

import unittest.mock
from typing import Any

import pytest
from garth.exc import GarthException
from garth.http import Client

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
        mock_client = unittest.mock.MagicMock()
        mock_storage_instance = unittest.mock.MagicMock()
        mock_storage_cls = unittest.mock.MagicMock(return_value=mock_storage_instance)
        mock_storage_instance.load.return_value = "token"
        
        with unittest.mock.patch.object("mcp_garmin.client.garth.http.client", mock_client):
            with unittest.mock.patch("mcp_garmin.client.FileTokenStorage", mock_storage_cls):
                client = GarminClient()
                result = client.get_client()
                
                assert result is mock_client
                assert mock_client.storage is mock_storage_instance
                assert mock_client.oauth2_token == "token"
                mock_storage_cls.assert_called_once()
                mock_storage_instance.load.assert_called_once()


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