"""This module defines an MCP server for Garmin data."""
import dataclasses
import logging
import json
from datetime import datetime, date, timezone
from typing import Annotated
from pydantic import Field
from mcp.server.mcpserver import MCPServer
from garth.exc import GarthException
import garmin_client

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
log = logging.getLogger(__name__)

server = MCPServer(name="mcp-garmin")

@server.tool()
def ping() -> str:
    """Health check tool to verify the MCP server responds."""
    return "pong"

@server.tool()
def get_sleep_summary(
    target_date: Annotated[
        date, Field(description="Date in ISO 8601 format (YYYY-MM-DD), e.g. 2023-09-13")
    ]
) -> dict:
    """Tool to retrieve sleep summary data for a specific date."""
    try:
        sleep_data = garmin_client.get_sleep_data(target_date)
        if sleep_data is None:
            return {"error": "No sleep data found for the specified date."}

        raw = dataclasses.asdict(sleep_data.daily_sleep_dto)
        log.debug("Raw sleep data: %s", json.dumps(raw, indent=2, default=str))

        result = {
            "sleep_start": datetime.fromtimestamp(
                raw["sleep_start_timestamp_local"] / 1000, tz=timezone.utc
                ).replace(tzinfo=None).isoformat(),
            "sleep_end": datetime.fromtimestamp(
                raw["sleep_end_timestamp_local"] / 1000, tz=timezone.utc
                ).replace(tzinfo=None).isoformat(),
            "average_respiration_value": raw["average_respiration_value"],
            "lowest_respiration_value": raw["lowest_respiration_value"],
            "highest_respiration_value": raw["highest_respiration_value"],
            "overall_sleep_score": raw["sleep_scores"]["overall"]["value"],
            "awake_count": raw["awake_count"],
            "sleep_score_insight": raw["sleep_score_insight"],
            "highest_sp_o2_value": raw["highest_sp_o2_value"],
            "lowest_sp_o2_value": raw["lowest_sp_o2_value"],
            "nap_time_minutes": raw["nap_time_seconds"] // 60,
            "total_sleep_minutes": raw["sleep_time_seconds"] // 60,
            "deep_sleep_minutes": raw["deep_sleep_seconds"] // 60,
            "light_sleep_minutes": raw["light_sleep_seconds"] // 60,
            "rem_sleep_minutes": raw["rem_sleep_seconds"] // 60,
            "awake_minutes": raw["awake_sleep_seconds"] // 60,
            "feedback": raw["sleep_score_feedback"],
            "overall_score_label": raw["sleep_scores"]["overall"]["qualifier_key"]
        }
        return result
    except GarthException as exc:
        return {"error": f"Garth error getting sleep data: {exc}"}
    except KeyError as exc:
        return {"error": f"Key not found in data: {exc}"}
