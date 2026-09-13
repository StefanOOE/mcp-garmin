"""This module defines an MCP server for Garmin data."""
import dataclasses
import logging
import json
from datetime import datetime, date, timezone
from typing import Annotated
from pydantic import BaseModel, Field
from mcp.server.mcpserver import MCPServer
from mcp.server.mcpserver.exceptions import ToolError
from garth.exc import GarthException
import garmin_client

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
log = logging.getLogger(__name__)

server = MCPServer(name="mcp-garmin")

class SleepSummary(BaseModel):
    """Pydantic model representing a sleep summary from Garmin."""
    sleep_start: str = Field(description="ISO 8601 timestamp when sleep started.")
    sleep_end: str = Field(description="ISO 8601 timestamp when sleep ended.")
    total_sleep_minutes: int = Field(description="Total time asleep, in minutes.")
    deep_sleep_minutes: int = Field(description="Minutes spent in deep sleep.")
    light_sleep_minutes: int = Field(description="Minutes spent in light sleep.")
    rem_sleep_minutes: int = Field(description="Minutes spent in REM sleep.")
    awake_minutes: int = Field(description="Minutes spent awake during the sleep window.")
    awake_count: int = Field(description="Number of times the user woke up.")
    nap_time_minutes: int = Field(description="Minutes napped, separate from main sleep.")
    overall_sleep_score: int = Field(description="Garmin overall sleep score, 0-100.")
    overall_score_label: str = Field(description="Qualitative label for the score, e.g. FAIR.")
    feedback: str = Field(description="Garmin's textual feedback code for the night.")
    sleep_score_insight: str = Field(description="Additional Garmin insight text, if any.")
    average_respiration_value: float = Field(description="Average breaths per minute.")
    lowest_respiration_value: float = Field(description="Lowest breaths per minute.")
    highest_respiration_value: float = Field(description="Highest breaths per minute.")
    lowest_sp_o2_value: int | None = Field(description="Lowest blood oxygen %, if measured.")
    highest_sp_o2_value: int | None = Field(description="Highest blood oxygen %, if measured.")

@server.tool()
def ping() -> str:
    """Health check tool to verify the MCP server responds."""
    return "pong"

@server.tool()
def get_sleep_summary(
    target_date: Annotated[
        date, Field(description="Date in ISO 8601 format (YYYY-MM-DD), e.g. 2023-09-13")
    ]
) -> SleepSummary:
    """Tool to retrieve sleep summary data for a specific date."""
    try:
        sleep_data = garmin_client.get_sleep_data(target_date)
        if sleep_data is None:
            raise ToolError("No sleep data found for the specified date.")

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
        return SleepSummary(**result)
    except GarthException as exc:
        raise ToolError(f"Garth error getting sleep data: {exc}") from exc
