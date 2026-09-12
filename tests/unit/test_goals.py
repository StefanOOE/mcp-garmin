"""Unit tests for goals tools."""
from __future__ import annotations

from unittest.mock import MagicMock, patch

from mcp_garmin.tools.goals import get_steps_goal, get_weight_goal, get_garmin_scores


def test_get_steps_goal():
    """Steps goal."""
    expected = {"device_goal": 10000, "user_goal": 12000}
    mock_client = MagicMock()
    
    with patch("garth.data.StepsGoal.get", return_value=MagicMock()):
        with patch("mcp_garmin.client.asdict", return_value=expected):
            result = get_steps_goal()
            assert result == expected


def test_get_steps_goal_none():
    """Steps goal handles None return."""
    mock_client = MagicMock()
    
    with patch("garth.data.StepsGoal.get", return_value=None):
        result = get_steps_goal()
        assert result == {}


def test_get_weight_goal():
    """Weight goal."""
    expected = {"user_goals": [95000], "user_goal_ranges": []}
    mock_client = MagicMock()
    
    with patch("garth.data.WeightGoal.get", return_value=MagicMock()):
        with patch("mcp_garmin.client.asdict", return_value=expected):
            result = get_weight_goal()
            assert result == expected


def test_get_weight_goal_none():
    """Weight goal handles None return."""
    mock_client = MagicMock()
    
    with patch("garth.data.WeightGoal.get", return_value=None):
        result = get_weight_goal()
        assert result == {}


def test_get_garmin_scores():
    """Garmin fitness scores."""
    expected = {"vo_2_max": 45.2, "endurance_score": 8.5}
    mock_client = MagicMock()
    
    with patch("garth.data.GarminScores.get", return_value=MagicMock()):
        with patch("mcp_garmin.client.asdict", return_value=expected):
            result = get_garmin_scores()
            assert result == expected


def test_get_garmin_scores_none():
    """Garmin fitness scores handles None return."""
    mock_client = MagicMock()
    
    with patch("garth.data.GarminScores.get", return_value=None):
        result = get_garmin_scores()
        assert result == {}