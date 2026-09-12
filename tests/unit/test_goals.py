"""Unit tests for goals tools."""
from __future__ import annotations

from unittest.mock import MagicMock, patch

from mcp_garmin.tools.goals import get_steps_goal, get_weight_goal, get_garmin_scores


def _patch_client(monkeypatch, mock_client):
    import mcp_garmin.tools.goals as goals

    monkeypatch.setattr(goals, "get_client", lambda: mock_client)


def test_get_steps_goal(monkeypatch):
    """Steps goal via connectapi endpoint fallback."""
    fixture = {"userStepGoal": 10000, "deviceStepGoal": 12000}
    expected = {"user_step_goal": 10000, "device_step_goal": 12000}
    mock_client = MagicMock()
    mock_client.connectapi.return_value = fixture
    _patch_client(monkeypatch, mock_client)

    result = get_steps_goal(day="2026-09-01")

    mock_client.connectapi.assert_called_once_with(
        "/wellness-service/wellness/wellness-goals/consolidated/steps/2026-09-01"
    )
    assert result == expected


def test_get_steps_goal_none(monkeypatch):
    """Steps goal handles empty/None connectapi response."""
    mock_client = MagicMock()
    mock_client.connectapi.return_value = None
    _patch_client(monkeypatch, mock_client)

    result = get_steps_goal(day="2026-09-01")
    assert result == {}


def test_get_weight_goal(monkeypatch):
    """Weight goal via connectapi endpoint fallback."""
    fixture = {"startWeight": 95000, "goalWeight": 90000}
    expected = {"start_weight": 95000, "goal_weight": 90000}
    mock_client = MagicMock()
    mock_client.connectapi.return_value = fixture
    _patch_client(monkeypatch, mock_client)

    result = get_weight_goal(day="2026-09-01")

    mock_client.connectapi.assert_called_once_with(
        "/goal-service/goal/user/effective/weightgoal/2026-09-01/2026-09-01"
    )
    assert result == expected


def test_get_weight_goal_none(monkeypatch):
    """Weight goal handles empty/None connectapi response."""
    mock_client = MagicMock()
    mock_client.connectapi.return_value = None
    _patch_client(monkeypatch, mock_client)

    result = get_weight_goal(day="2026-09-01")
    assert result == {}


def test_get_garmin_scores(monkeypatch):
    """Garmin fitness scores via GarminScoresData accessor."""
    expected = {"vo_2_max": 45.2, "endurance_score": 8.5}
    mock_client = MagicMock()
    _patch_client(monkeypatch, mock_client)

    with patch(
        "garth.data.GarminScoresData.get", return_value=MagicMock()
    ) as mock_get:
        with patch("mcp_garmin.tools.goals._to_dict", return_value=expected):
            result = get_garmin_scores(day="2026-09-01")

    mock_get.assert_called_once_with(day="2026-09-01", client=mock_client)
    assert result == expected


def test_get_garmin_scores_none(monkeypatch):
    """Garmin fitness scores handles None return (no Hill/Endurance data)."""
    mock_client = MagicMock()
    _patch_client(monkeypatch, mock_client)

    with patch("garth.data.GarminScoresData.get", return_value=None):
        result = get_garmin_scores(day="2026-09-01")
    assert result == {}
