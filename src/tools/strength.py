"""Strength training exercise sets tool backed by garmin_client/garth."""
import logging
import json
from typing import Annotated
from pydantic import BaseModel, Field
from mcp.server.mcpserver.exceptions import ToolError
from garth.exc import GarthException
import garmin_client
from server_instance import server

log = logging.getLogger(__name__)

class ExerciseSet(BaseModel):
    """Pydantic model representing a single set of a strength training activity."""
    set_type: str = Field(
        description="Type of the set: ACTIVE (exercise performed) or REST (pause)."
    )
    start_utc: str | None = Field(
        description="ISO 8601 timestamp in UTC when the set started (not set for REST sets)."
    )
    duration: float | None = Field(
        description="Duration of the set, in seconds."
    )
    repetitions: int | None = Field(
        description="Number of repetitions performed, if an ACTIVE set."
    )
    weight_kg: float | None = Field(
        description="Weight used, in kilograms (0.0 means bodyweight), if an ACTIVE set."
    )
    exercise_category: str | None = Field(
        description="Garmin exercise category, e.g. SQUAT or DEADLIFT, if recognized."
    )
    exercise_name: str | None = Field(
        description="Specific Garmin exercise name, e.g. BARBELL_BACK_SQUAT, if known."
    )

class StrengthWorkout(BaseModel):
    """Pydantic model representing the exercise sets of a strength training activity."""
    activity_id: int = Field(
        description="Unique identifier for the activity."
    )
    sets: list[ExerciseSet] = Field(
        description="Sets of the activity in chronological order."
    )

def _to_utc_iso(start_time: str | None) -> str | None:
    """Mark Garmin's offset-less UTC startTime (e.g. '2026-09-25T13:32:30.0') as UTC."""
    return f"{start_time}Z" if start_time else None

def _to_kg(weight_grams: float | None) -> float | None:
    """Convert Garmin's weight in grams to kilograms; negative values mean 'no weight'."""
    if weight_grams is None or weight_grams < 0:
        return None
    return weight_grams / 1000

def _to_exercise_set(raw_set: dict) -> ExerciseSet:
    """Map one raw Garmin exercise set to an ExerciseSet (first exercise candidate wins)."""
    exercises = raw_set.get("exercises") or [{}]
    return ExerciseSet(
        set_type=raw_set.get("setType", "unknown"),
        start_utc=_to_utc_iso(raw_set.get("startTime")),
        duration=raw_set.get("duration"),
        repetitions=raw_set.get("repetitionCount"),
        weight_kg=_to_kg(raw_set.get("weight")),
        exercise_category=exercises[0].get("category"),
        exercise_name=exercises[0].get("name"),
    )

@server.tool()
def get_strength_exercises(
    activity_id: Annotated[
        int, Field(description="Unique identifier for the strength training activity.")
    ],
    include_rest: Annotated[
        bool, Field(description="Whether to include REST sets (pauses between sets).")
    ] = False,
) -> StrengthWorkout:
    """Tool to retrieve the exercises of a strength training activity: exercise,
       repetitions, weight and duration per set."""
    try:
        raw = garmin_client.get_exercise_sets(activity_id)
        log.debug("Raw exercise sets: %s", json.dumps(raw, indent=2, default=str))

        raw_sets = (raw or {}).get("exerciseSets")
        if not raw_sets:
            raise ToolError(f"No exercise sets found for activity ID {activity_id}.")

        sets = [_to_exercise_set(raw_set) for raw_set in raw_sets]
        if not include_rest:
            sets = [exercise_set for exercise_set in sets if exercise_set.set_type != "REST"]
        return StrengthWorkout(activity_id=activity_id, sets=sets)
    except GarthException as exc:
        raise ToolError(f"Garth error getting exercise sets: {exc}") from exc

# ============= sample exercise sets data from garth (strength session, shortened)=============
# {
#  "activityId": 24494119479,
#  "exerciseSets": [
#   {
#    "exercises": [{"category": "SQUAT", "name": "BARBELL_BACK_SQUAT", "probability": 100.0}],
#    "duration": 48.601,
#    "repetitionCount": 8,
#    "weight": 20000.0,                    <- grams
#    "setType": "ACTIVE",
#    "startTime": "2026-09-25T13:34:20.0", <- UTC (local start was 15:34)
#    "wktStepIndex": null,
#    "messageIndex": null,
#    "avgConcentricMeanVelocity": null,    <- ~20 velocity-based-training fields,
#    ...                                      all null without a velocity sensor
#   },
#   {
#    "exercises": [],
#    "duration": 84.11,
#    "repetitionCount": null,
#    "weight": -1.0,
#    "setType": "REST",
#    "startTime": null,
#    ...
#   }
#  ]
# }
# Non-strength activities (e.g. cycling) return {"activityId": ..., "exerciseSets": null}.
# ============= end sample exercise sets data from garth (strength session)=============
