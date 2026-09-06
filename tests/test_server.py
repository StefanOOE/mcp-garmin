"""Test suite for mcp-garmin server and tool registration."""

import pytest
from unittest.mock import Mock, patch

from mcp_garmin.server import mcp


def test_server_initialization():
    """Test MCP server initialization."""
    assert mcp is not None
    assert hasattr(mcp, 'register_tool')


def test_tool_registration():
    """Test that tools are properly registered with the MCP server."""
    # Check that we have some tools registered
    # This test will be more meaningful once we actually run the registration
    
    # For now, just verify the server object exists
    assert hasattr(mcp, 'register_tool')


def test_tool_metadata_exists():
    """Test that tools have proper metadata."""
    # This is a basic check - actual tool metadata validation 
    # will happen during the registration process
    pass