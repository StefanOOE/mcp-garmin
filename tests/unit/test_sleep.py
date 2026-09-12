"""Unit tests for sleep tools."""
from __future__ import annotations

from unittest.mock import MagicMock, patch

from mcp_garmin.tools.sleep import get_sleep, get_sleep_detail, get_sleep_summary


def test_get_sleep():
    """Sleep data for a day (YYYY-MM-DD)."""
    fixture = {"sleep_time_seconds": 25200, "calendar_date": "2026-09-01"}
    mock_client = MagicMock()
    
    with patch("garth.data.SleepData.get", return_value=fixture) as mock_get:
        result = get_sleep(day="2026-09-01")
    
    mock_get.assert_called_once()
    assert mock_get.call_args.kwargs["day"] == "2026-09-01"
    assert result == fixture


def test_get_sleep_detail():
    """Detailed sleep data for a day (YYYY-MM-DD)."""
    fixture = {
        "sleep_start_timestamp_gmt": 1788100000000,
        "sleep_end_timestamp_gmt": 1788190000000,
    }
    mock_client = MagicMock()
    
    with patch("garth.data.DailySleepData.get", return_value=fixture) as mock_get:
        result = get_sleep_detail(day="2026-09-01")
    
    mock_get.assert_called_once()
    assert mock_get.call_args.kwargs["day"] == "2026-09-01"
    assert result == fixture


def test_get_sleep_summary_extracts_sleep_fields():
    """Sleep summary extracts sleep fields."""
    full = {
        "calendar_date": "2026-08-31",
        "total_steps": 20882,
        "resting_heart_rate": 52,
        "sleeping_seconds": 25200,
        "sleep_start_timestamp_gmt": 1788100000000,
    }
    mock_client = MagicMock()
    
    with patch("garth.data.DailySummary.get", return_value=full) as mock_get:
        result = get_sleep_summary(day="2026-08-31")
    
    mock_get.assert_called_once()
    assert result == {
        "sleeping_seconds": 25200,
        "sleep_start_timestamp_gmt": 1788100000000,
    }


def test_get_sleep_summary_returns_full_when_no_sleep_fields():
    """Sleep summary returns full when no sleep fields."""
    full = {"calendar_date": "2026-08-31", "total_steps": 20882}
    mock_client = MagicMock()
    
    with patch("garth.data.DailySummary.get", return_value=full):
        result = get_sleep_summary(day="2026-08-31")
    
    assert result == full


def test_get_sleep_summary_none():
    """Sleep summary handles None."""
    mock_client = MagicMock()
    
    with patch("garth.data.DailySummary.get", return_value=None):
        result = get_sleep_summary(day="2026-08-31")
    
    assert result == {}