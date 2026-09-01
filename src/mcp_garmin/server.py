"""MCP server exposing Garmin Connect fitness data as tools."""
from __future__ import annotations

from mcp.server import MCPServer

mcp = MCPServer(
    "mcp-garmin",
    version="0.1.0",
    instructions=(
        "Garmin Connect fitness data as fine-grained MCP tools. "
        "Returns snake_case JSON dicts. Use get_user_profile() for identity, "
        "get_body_weight() for weight, get_sleep_summary() for sleep, "
        "get_hrv() for HRV, get_daily_stress() for stress. "
        "All timestamps are ISO 8601 or YYYY-MM-DD date strings. "
        "Weight is in grams (e.g. 95010 = 95.01 kg). Steps are integers. "
        "Calories are in kcal. If a tool returns a German ToolError message, "
        "the Garmin token is likely expired — re-run garmin_login.py."
    ),
)


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
