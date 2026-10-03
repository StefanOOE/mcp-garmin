"""Calories tool: daily energy expenditure (total = active + resting) from Garmin."""
import json
import logging
from datetime import date
from typing import Annotated
from pydantic import BaseModel, Field
from mcp.server.mcpserver.exceptions import ToolError
from garth.exc import GarthException
import garmin_client
from server_instance import server

log = logging.getLogger(__name__)

MAX_PERIOD_DAYS = 31

class CalorieSummary(BaseModel):
    """Pydantic model representing one day's calorie expenditure from Garmin."""
    date: str = Field(
        description="ISO 8601 calendar date the values apply to."
    )
    total_kilocalories: float | None = Field(
        description="Total calories burned (active + resting), if measured. For today this is "
                    "the value so far, not a projection for the whole day."
    )
    active_kilocalories: float | None = Field(
        description="Calories burned through activity and movement, if measured."
    )
    resting_kilocalories: float | None = Field(
        description="Resting calories (basal metabolic rate, BMR), if measured."
    )
    calorie_goal: int | None = Field(
        description="Net calorie goal configured in Garmin Connect, if set."
    )

@server.tool()
def get_calorie_summary(
    target_date: Annotated[
        date, Field(description="Date in ISO 8601 format (YYYY-MM-DD), e.g. 2023-09-13")
    ],
    period: Annotated[
        int, Field(ge=1, le=MAX_PERIOD_DAYS,
                   description="Number of days up to and including the target date (1-31).")
    ] = 1,
) -> list[CalorieSummary]:
    """Tool to retrieve the daily calorie expenditure (total = active + resting calories)
    for a target date and the days before it."""
    try:
        summaries = garmin_client.get_daily_summaries(target_date, period)
    except GarthException as exc:
        raise ToolError(f"Garth error getting calorie data: {exc}") from exc

    result = []
    for raw in summaries:
        log.debug("Raw daily summary: %s", json.dumps(raw, indent=2, default=str))
        result.append(CalorieSummary(
            date=raw.get("calendarDate", "unknown"),
            total_kilocalories=raw.get("totalKilocalories"),
            active_kilocalories=raw.get("activeKilocalories"),
            resting_kilocalories=raw.get("bmrKilocalories"),
            calorie_goal=raw.get("netCalorieGoal"),
        ))
    return result

# ======== daily summary sample (calorie fields only, anonymized) ========
# call: garth.connectapi("/usersummary-service/usersummary/daily/?calendarDate=2026-10-02")
# =========================================================================
#   "calendarDate": "2026-10-02",
#   "totalKilocalories": 2612.0,
#   "activeKilocalories": 370.0,
#   "bmrKilocalories": 2242.0,
#   "wellnessKilocalories": 2612.0,
#   "netCalorieGoal": 2000,
#   "restingCaloriesFromActivity": 119.0
