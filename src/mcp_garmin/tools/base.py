"""Base tool registry and decorators."""

from __future__ import annotations

from typing import Any, Callable

from mcp.server import MCPServer

# Global MCP server instance
mcp = MCPServer(
    "mcp-garmin",
    version="0.1.0",
    instructions=(
        "Garmin Connect fitness data as fine-grained MCP tools. "
        "Returns snake_case JSON dicts. Use get_user_profile() for identity, "
        "get_body_weight() for weight, get_sleep_summary() for sleep, "
        "get_daily_heart_rate() for HR, get_daily_stress() for stress. "
        "All timestamps are ISO 8601 or YYYY-MM-DD date strings. "
        "Weight is in grams (e.g. 95010 = 95.01 kg). Steps are integers. "
        "If a tool returns a ToolError, "
        "the Garmin token is likely expired — re-run garmin_login.py."
    ),
)


def register(mcp_server: MCPServer, name: str | None = None) -> Callable:
    """Register a tool with the MCP server."""
    def decorator(func: Callable) -> Callable:
        tool_name = name or func.__name__
        mcp_server.tool(name=tool_name)(func)
        return func
    return decorator