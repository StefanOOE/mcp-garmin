"""Sleep summary tool backed by garmin_client/garth."""
import dataclasses
import logging
import json
from datetime import datetime, date, timezone
from typing import Annotated
from pydantic import BaseModel, Field
from mcp.server.mcpserver.exceptions import ToolError
from garth.exc import GarthException
import garmin_client
from server_instance import server

log = logging.getLogger(__name__)


def _local_iso(raw: dict, key: str) -> str:
    """Convert a Garmin *_timestamp_local epoch-ms field to an ISO string.

    Garmin's API has no version field to detect a renamed/missing key against
    (see README disclaimer), so this degrades to "unknown" instead of crashing
    the whole tool if the field is ever absent.
    """
    timestamp_ms = raw.get(key)
    if timestamp_ms is None:
        return "unknown"
    local_dt = datetime.fromtimestamp(timestamp_ms / 1000, tz=timezone.utc)
    return local_dt.replace(tzinfo=None).isoformat()


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

        overall_score = raw.get("sleep_scores", {}).get("overall", {})
        result = {
            "sleep_start": _local_iso(raw, "sleep_start_timestamp_local"),
            "sleep_end": _local_iso(raw, "sleep_end_timestamp_local"),
            "average_respiration_value": raw.get("average_respiration_value", 0.0),
            "lowest_respiration_value": raw.get("lowest_respiration_value", 0.0),
            "highest_respiration_value": raw.get("highest_respiration_value", 0.0),
            "overall_sleep_score": overall_score.get("value", 0),
            "awake_count": raw.get("awake_count", 0),
            "sleep_score_insight": raw.get("sleep_score_insight", "UNKNOWN"),
            "highest_sp_o2_value": raw.get("highest_sp_o2_value"),
            "lowest_sp_o2_value": raw.get("lowest_sp_o2_value"),
            "nap_time_minutes": raw.get("nap_time_seconds", 0) // 60,
            "total_sleep_minutes": raw.get("sleep_time_seconds", 0) // 60,
            "deep_sleep_minutes": raw.get("deep_sleep_seconds", 0) // 60,
            "light_sleep_minutes": raw.get("light_sleep_seconds", 0) // 60,
            "rem_sleep_minutes": raw.get("rem_sleep_seconds", 0) // 60,
            "awake_minutes": raw.get("awake_sleep_seconds", 0) // 60,
            "feedback": raw.get("sleep_score_feedback", "UNKNOWN"),
            "overall_score_label": overall_score.get("qualifier_key", "UNKNOWN"),
        }
        return SleepSummary(**result)
    except GarthException as exc:
        raise ToolError(f"Garth error getting sleep data: {exc}") from exc
