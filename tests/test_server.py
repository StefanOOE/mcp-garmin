"""Smoke tests for mcp_garmin.server."""
from mcp.server import MCPServer


def test_server_importable():
    from mcp_garmin.server import mcp
    assert isinstance(mcp, MCPServer)


def test_server_name_and_version():
    from mcp_garmin.server import mcp
    assert mcp.name == "mcp-garmin"
    assert mcp.version == "0.1.0"
