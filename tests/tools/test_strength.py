"""Tests for tools.strength: field mapping from a fake Garth exerciseSets response
to StrengthWorkout/ExerciseSet."""
from unittest.mock import patch
import pytest
from garth.exc import GarthException
from mcp.server.mcpserver.exceptions import ToolError

from tools.strength import get_strength_exercises

@pytest.fixture(name="fake_exercise_sets")
def _build_fake_exercise_sets() -> dict:
    """A minimal, realistic fake exerciseSets response, built from real field
    values recorded during manual testing (strength session 2026-09-25)."""
    return {
        "activityId": 24494119479,
        "exerciseSets": [
            {
                "exercises": [{"category": "SQUAT", "name": None, "probability": 100.0}],
                "duration": 38.591,
                "repetitionCount": 10,
                "weight": 0.0,
                "setType": "ACTIVE",
                "startTime": "2026-09-25T13:32:30.0",
            },
            {
                "exercises": [],
                "duration": 71.716,
                "repetitionCount": None,
                "weight": -1.0,
                "setType": "REST",
                "startTime": None,
            },
            {
                "exercises": [
                    {"category": "SQUAT", "name": "BARBELL_BACK_SQUAT", "probability": 100.0}
                ],
                "duration": 48.601,
                "repetitionCount": 8,
                "weight": 20000.0,
                "setType": "ACTIVE",
                "startTime": "2026-09-25T13:34:20.0",
            },
        ],
    }

@patch("garmin_client.login")
@patch("garth.connectapi")
def test_get_strength_exercises_maps_fields(mock_connectapi, mock_login, fake_exercise_sets):
    """The happy path: REST sets are skipped by default, weight is converted
    from grams to kg, and the UTC start time is marked as such."""
    mock_connectapi.return_value = fake_exercise_sets

    result = get_strength_exercises(24494119479)

    assert result.activity_id == 24494119479
    assert len(result.sets) == 2
    bodyweight, barbell = result.sets
    assert bodyweight.set_type == "ACTIVE"
    assert bodyweight.start_utc == "2026-09-25T13:32:30.0Z"
    assert bodyweight.repetitions == 10
    assert bodyweight.weight_kg == 0.0
    assert bodyweight.exercise_category == "SQUAT"
    assert bodyweight.exercise_name is None
    assert barbell.weight_kg == 20.0
    assert barbell.exercise_name == "BARBELL_BACK_SQUAT"
    assert barbell.duration == 48.601
    mock_connectapi.assert_called_once_with(
        "/activity-service/activity/24494119479/exerciseSets"
    )
    mock_login.assert_called_once()

@patch("garmin_client.login")
@patch("garth.connectapi")
def test_get_strength_exercises_includes_rest_on_request(
    mock_connectapi, mock_login, fake_exercise_sets
):
    """With include_rest, REST sets are returned with no weight/exercise/start."""
    mock_connectapi.return_value = fake_exercise_sets

    result = get_strength_exercises(24494119479, include_rest=True)

    assert len(result.sets) == 3
    rest = result.sets[1]
    assert rest.set_type == "REST"
    assert rest.start_utc is None
    assert rest.weight_kg is None
    assert rest.repetitions is None
    assert rest.exercise_category is None
    assert rest.duration == 71.716
    mock_login.assert_called_once()

@pytest.mark.parametrize("response", [None, {"activityId": 1, "exerciseSets": None}])
@patch("garmin_client.login")
@patch("garth.connectapi")
def test_get_strength_exercises_raises_tool_error_when_no_sets(
    mock_connectapi, mock_login, response
):
    """Non-strength activities (e.g. cycling) return exerciseSets: null - an
    anticipated failure with a specific, LLM-readable message."""
    mock_connectapi.return_value = response

    with pytest.raises(ToolError, match="No exercise sets found"):
        get_strength_exercises(1)
    mock_login.assert_called_once()

@patch("garmin_client.login")
@patch("garth.connectapi")
def test_get_strength_exercises_wraps_garth_exception(mock_connectapi, mock_login):
    """A Garth failure surfaces as a ToolError, not a raw exception."""
    mock_connectapi.side_effect = GarthException(msg="boom")

    with pytest.raises(ToolError, match="Garth error getting exercise sets"):
        get_strength_exercises(1)
    mock_login.assert_called_once()
