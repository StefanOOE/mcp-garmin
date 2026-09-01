"""Tests for goals.py."""
from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest


@pytest.fixture
def mock_client(monkeypatch):
    """Patches get_client to return a MagicMock."""
    client = MagicMock()
    monkeypatch.setattr("mcp_garmin.client._client", client)
    return client


class TestStepsGoal:
    def test_returns_dict(self, mock_client):
        from mcp_garmin.goals import get_steps_goal

        expected = {"device_goal": 10000, "user_goal": 12000}
        with patch("garth.data.StepsGoal.get", return_value=MagicMock()):
            with patch("mcp_garmin.client.asdict", return_value=expected):
                result = get_steps_goal(day="2026-09-01")
                assert result == expected

    def test_handles_none(self, mock_client):
        from mcp_garmin.goals import get_steps_goal

        with patch("garth.data.StepsGoal.get", return_value=None):
            result = get_steps_goal()
            assert result == {}


class TestWeightGoal:
    def test_returns_dict(self, mock_client):
        from mcp_garmin.goals import get_weight_goal

        expected = {"user_goals": [95000], "user_goal_ranges": []}
        with patch("garth.data.WeightGoal.get", return_value=MagicMock()):
            with patch("mcp_garmin.client.asdict", return_value=expected):
                result = get_weight_goal(day="2026-09-01")
                assert result == expected

    def test_handles_none(self, mock_client):
        from mcp_garmin.goals import get_weight_goal

        with patch("garth.data.WeightGoal.get", return_value=None):
            result = get_weight_goal()
            assert result == {}


class TestGarminScores:
    def test_returns_dict(self, mock_client):
        from mcp_garmin.goals import get_garmin_scores

        expected = {"vo_2_max": 45.2, "endurance_score": 8.5}
        with patch("garth.GarminScoresData.get", return_value=MagicMock()):
            with patch("mcp_garmin.client.asdict", return_value=expected):
                result = get_garmin_scores(day="2026-09-01")
                assert result == expected

    def test_handles_none(self, mock_client):
        from mcp_garmin.goals import get_garmin_scores

        with patch("garth.GarminScoresData.get", return_value=None):
            result = get_garmin_scores()
            assert result == {}
