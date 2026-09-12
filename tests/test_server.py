"""Test suite for mcp-garmin server and tool registration."""

from mcp_garmin.server import mcp


def test_server_initialization():
    """Test MCP server initialization."""
    assert mcp is not None
    assert hasattr(mcp, "tool")


def test_tool_registration():
    """Test that tools are registered with the MCP server (via .list_tools())."""
    import asyncio

    tools = asyncio.run(mcp.list_tools())
    assert len(tools) > 0


def test_tool_metadata_exists():
    """Test that tools have proper metadata."""
    import asyncio

    tools = asyncio.run(mcp.list_tools())
    assert all(t.name for t in tools)
