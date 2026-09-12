"""Unit tests for stress tools."""
from __future__ import annotations

from unittest.mock import patch

from mcp_garmin.tools.stress import (
    get_daily_stress,
    get_weekly_stress,
    get_training_status_daily,
    get_training_status_weekly,
    get_training_status_monthly,
    get_training_readiness,
    get_morning_readiness,
)


def test_get_daily_stress():
    """Daily stress data for a day (YYYY-MM-DD)."""
    fixture = {"stress_level": 50, "calendar_date": "2026-08-31"}

    with patch("garth.stats.DailyStress.list", return_value=[fixture]) as mock_list:
        with patch("mcp_garmin.client.asdict", return_value=fixture):
            result = get_daily_stress(day="2026-08-31")

    mock_list.assert_called_once()
    assert mock_list.call_args.kwargs["end"] == "2026-08-31"
    assert mock_list.call_args.kwargs["period"] == 1
    assert result == fixture


def test_get_weekly_stress():
    """Weekly stress data starting from a date (YYYY-MM-DD)."""
    fixture = {"stress_level": 50, "calendar_date": "2026-08-31"}

    with patch("garth.stats.WeeklyStress.list", return_value=[fixture]) as mock_list:
        with patch("mcp_garmin.client.asdict", return_value=fixture):
            result = get_weekly_stress(end="2026-08-31", period=1)

    mock_list.assert_called_once()
    assert mock_list.call_args.kwargs["end"] == "2026-08-31"
    assert mock_list.call_args.kwargs["period"] == 1
    assert result == [fixture]


def test_get_training_status_daily():
    """Training status for a day (YYYY-MM-DD)."""
    fixture = {"training_readiness_score": 72, "calendar_date": "2026-09-01"}

    with patch(
        "garth.stats.training_status.DailyTrainingStatus.list", return_value=[fixture]
    ) as mock_list:
        with patch("mcp_garmin.client.asdict", return_value=fixture):
            result = get_training_status_daily(end="2026-09-01")

    mock_list.assert_called_once()
    assert mock_list.call_args.kwargs["end"] == "2026-09-01"
    assert result == [fixture]


def test_get_training_status_weekly():
    """Training status for a week starting from a date (YYYY-MM-DD)."""
    fixture = {"training_readiness_score": 70}

    with patch(
        "garth.stats.training_status.WeeklyTrainingStatus.list", return_value=[fixture]
    ) as mock_list:
        with patch("mcp_garmin.client.asdict", return_value=fixture):
            result = get_training_status_weekly(end="2026-09-01")

    mock_list.assert_called_once()
    assert mock_list.call_args.kwargs["end"] == "2026-09-01"
    assert result == [fixture]


def test_get_training_status_monthly():
    """Training status for a month starting from a date (YYYY-MM-DD)."""
    fixture = {"training_readiness_score": 65}

    with patch(
        "garth.stats.training_status.MonthlyTrainingStatus.list",
        return_value=[fixture],
    ) as mock_list:
        with patch("mcp_garmin.client.asdict", return_value=fixture):
            result = get_training_status_monthly(end="2026-09-01")

    mock_list.assert_called_once()
    assert mock_list.call_args.kwargs["end"] == "2026-09-01"
    assert result == [fixture]


def test_get_training_status_none_returns_empty_list():
    """Training status handles empty-list return."""
    with patch(
        "garth.stats.training_status.DailyTrainingStatus.list", return_value=[]
    ):
        assert get_training_status_daily(end="2026-09-01") == []


def test_get_training_readiness():
    """Training readiness for a day (YYYY-MM-DD)."""
    fixture = {"training_readiness_score": 72, "calendar_date": "2026-09-01"}

    with patch(
        "garth.data.TrainingReadinessData.get", return_value=[fixture]
    ) as mock_get:
        with patch("mcp_garmin.client.asdict", return_value=fixture):
            result = get_training_readiness(day="2026-09-01")

    mock_get.assert_called_once()
    assert mock_get.call_args.kwargs["day"] == "2026-09-01"
    assert result == [fixture]


def test_get_morning_readiness():
    """Morning readiness for a day (YYYY-MM-DD)."""
    fixture = {"training_readiness_score": 72}

    with patch(
        "garth.data.MorningTrainingReadinessData.get", return_value=fixture
    ) as mock_get:
        with patch("mcp_garmin.client.asdict", return_value=fixture):
            result = get_morning_readiness(day="2026-09-01")

    mock_get.assert_called_once()
    assert mock_get.call_args.kwargs["day"] == "2026-09-01"
    assert result == fixture
