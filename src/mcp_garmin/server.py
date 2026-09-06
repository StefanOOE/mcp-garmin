"""MCP server exposing Garmin Connect fitness data as tools."""

from __future__ import annotations

from mcp.server import MCPServer

# Import all tool functions from their respective modules in the tools directory
from .tools.base import get_registered_tools
from .tools.body import *
from .tools.heart import *
from .tools.sleep import *
from .tools.stress import *
from .tools.steps import *
from .tools.hydration import *
from .tools.activity import *
from .tools.devices import *
from .tools.nutrition import *
from .tools.goals import *
from .tools.util import *

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

# Register all tools using the registry
for tool in get_registered_tools():
    mcp.tool()(tool)


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
