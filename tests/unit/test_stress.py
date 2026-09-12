"""Unit tests for stress tools."""
from __future__ import annotations

from unittest.mock import MagicMock, patch

from mcp_garmin.tools.stress import get_daily_stress, get_weekly_stress, get_training_status_daily, get_training_status_weekly, get_training_status_monthly, get_training_readiness, get_morning_readiness


def test_get_daily_stress():
    """Daily stress data for a day (YYYY-MM-DD)."""
    fixture = {"stress_level": 50, "calendar_date": "2026-08-31"}
    mock_client = MagicMock()
    
    with patch("garth.data.DailyStressData.get", return_value=[fixture]) as mock_get:
        result = get_daily_stress(end="2026-08-31", days=1)
    
    mock_get.assert_called_once()
    assert mock_get.call_args.kwargs["end"] == "2026-08-31"
    assert mock_get.call_args.kwargs["period"] == 1
    assert result == [fixture]


def test_get_weekly_stress():
    """Weekly stress data starting from a date (YYYY-MM-DD)."""
    fixture = {"stress_level": 50, "calendar_date": "2026-08-31"}
    mock_client = MagicMock()
    
    with patch("garth.data.WeeklyStressData.get", return_value=[fixture]) as mock_get:
        result = get_weekly_stress(end="2026-08-31")
    
    mock_get.assert_called_once()
    assert mock_get.call_args.kwargs["end"] == "2026-08-31"
    assert mock_get.call_args.kwargs["period"] == 7
    assert result == [fixture]


def test_get_training_status_daily():
    """Training status for a day (YYYY-MM-DD)."""
    fixture = {"training_readiness_score": 72, "calendar_date": "2026-09-01"}
    mock_client = MagicMock()
    
    with patch("garth.data.TrainingStatusDaily.get", return_value=fixture) as mock_get:
        result = get_training_status_daily(day="2026-09-01")
    
    mock_get.assert_called_once()
    assert mock_get.call_args.kwargs["day"] == "2026-09-01"
    assert result == fixture


def test_get_training_status_weekly():
    """Training status for a week starting from a date (YYYY-MM-DD)."""
    fixture = {"training_readiness_score": 70}
    mock_client = MagicMock()
    
    with patch("garth.data.TrainingStatusWeekly.get", return_value=fixture) as mock_get:
        result = get_training_status_weekly(end="2026-09-01")
    
    mock_get.assert_called_once()
    assert mock_get.call_args.kwargs["day"] == "2026-09-01"
    assert result == fixture


def test_get_training_status_monthly():
    """Training status for a month starting from a date (YYYY-MM-DD)."""
    fixture = {"training_readiness_score": 65}
    mock_client = MagicMock()
    
    with patch("garth.data.TrainingStatusMonthly.get", return_value=fixture) as mock_get:
        result = get_training_status_monthly(end="2026-09-01")
    
    mock_get.assert_called_once()
    assert mock_get.call_args.kwargs["day"] == "2026-09-01"
    assert result == fixture


def test_get_training_status_none_returns_empty_list():
    """Training status handles None return."""
    mock_client = MagicMock()
    
    with patch("garth.data.TrainingReadinessData.get", return_value=None):
        assert get_training_status_daily(day="2026-09-01") == []


def test_get_training_readiness():
    """Training readiness for a day (YYYY-MM-DD)."""
    fixture = {"training_readiness_score": 72, "calendar_date": "2026-09-01"}
    mock_client = MagicMock()
    
    with patch("garth.data.TrainingReadiness.get", return_value=fixture) as mock_get:
        result = get_training_readiness(day="2026-09-01")
    
    mock_get.assert_called_once()
    assert mock_get.call_args.kwargs["day"] == "2026-09-01"
    assert result == fixture


def test_get_morning_readiness():
    """Morning readiness for a day (YYYY-MM-DD)."""
    fixture = {"training_readiness_score": 72}
    mock_client = MagicMock()
    
    with patch("garth.data.MorningReadiness.get", return_value=fixture) as mock_get:
        result = get_morning_readiness(day="2026-09-01")
    
    mock_get.assert_called_once()
    assert mock_get.call_args.kwargs["day"] == "2026-09-01"
    assert result == fixture