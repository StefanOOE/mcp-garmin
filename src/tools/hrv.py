"""HRV summary tool backed by garmin_client/garth."""
import dataclasses
import logging
import json
from datetime import date
from typing import Annotated
from pydantic import BaseModel, Field
from mcp.server.mcpserver.exceptions import ToolError
from garth.exc import GarthException
import garmin_client
from server_instance import server
from tools._shared import local_iso

log = logging.getLogger(__name__)

class HRVSummary(BaseModel):
    """Pydantic model representing a heart rate variability (HRV) summary from Garmin."""
    hrv_sleep_start: str = Field(description="ISO 8601 timestamp when sleep started.")
    hrv_sleep_end: str = Field(description="ISO 8601 timestamp when sleep ended.")
    hrv_feedback: str = Field(description="Garmin's textual feedback code for the HRV measurement.")
    hrv_last_night_avg: float = Field(description="Average HRV value from the last night (ms)")
    hrv_weekly_avg: float = Field(description="Average HRV value over the last week (ms).")

@server.tool()
def get_hrv_summary(
    target_date: Annotated[
        date, Field(description="Date in ISO 8601 format (YYYY-MM-DD), e.g. 2023-09-13")
    ]
) -> HRVSummary:
    """Tool to retrieve heart rate variability (HRV) summary data for a specific date."""
    try:
        hrv_data = garmin_client.get_hrv_data(target_date)
        if hrv_data is None:
            raise ToolError("No HRV data found for the specified date.")

        raw = dataclasses.asdict(hrv_data)
        log.debug("Raw HRV data: %s", json.dumps(raw, indent=2, default=str))

        result = {
            "hrv_sleep_start": local_iso(raw.get("sleep_start_timestamp_local")),
            "hrv_sleep_end": local_iso(raw.get("sleep_end_timestamp_local")),
            "hrv_feedback": raw.get("hrv_summary", {}).get("status", "unknown"),
            "hrv_last_night_avg": raw.get("hrv_summary", {}).get("last_night_avg", 0.0),
            "hrv_weekly_avg": raw.get("hrv_summary", {}).get("weekly_avg", 0.0)
        }

        return HRVSummary(**result)
    except GarthException as exc:
        raise ToolError(f"Garth error getting HRV data: {exc}") from exc
