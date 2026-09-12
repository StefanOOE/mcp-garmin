"""Unit tests for sleep tools."""
from __future__ import annotations

from unittest.mock import MagicMock, patch

from mcp_garmin.tools.sleep import get_sleep, get_sleep_detail, get_sleep_summary


def test_get_sleep():
    """Sleep data for a day (YYYY-MM-DD) -- daily_sleep_dto + movement."""
    fake_result = MagicMock()
    dto_fixture = {"sleep_time_seconds": 25200, "calendar_date": "2026-09-01"}
    fake_result.daily_sleep_dto = MagicMock()
    fake_result.sleep_movement = []

    with patch("garth.data.SleepData.get", return_value=fake_result) as mock_get:
        with patch("mcp_garmin.client.asdict", return_value=dto_fixture):
            result = get_sleep(day="2026-09-01")

    mock_get.assert_called_once()
    assert mock_get.call_args.kwargs["day"] == "2026-09-01"
    assert result == [dict(dto_fixture, sleep_movement=[])]


def test_get_sleep_none_returns_empty_list():
    """SleepData.get returns None -> []."""
    with patch("garth.data.SleepData.get", return_value=None):
        result = get_sleep(day="2026-09-01")

    assert result == []


def test_get_sleep_detail():
    """Detailed sleep data for a day (YYYY-MM-DD)."""
    fixture = {
        "sleep_start_timestamp_gmt": 1788100000000,
        "sleep_end_timestamp_gmt": 1788190000000,
    }

    with patch("garth.data.DailySleepData.get", return_value=MagicMock()) as mock_get:
        with patch("mcp_garmin.client.asdict", return_value=fixture):
            result = get_sleep_detail(day="2026-09-01")

    mock_get.assert_called_once()
    assert mock_get.call_args.kwargs["day"] == "2026-09-01"
    assert result == fixture


def test_get_sleep_detail_none_returns_empty_dict():
    """DailySleepData.get returns None -> {}."""
    with patch("garth.data.DailySleepData.get", return_value=None):
        result = get_sleep_detail(day="2026-09-01")

    assert result == {}


def test_get_sleep_summary():
    """Sleep summary for a day (YYYY-MM-DD) -- scores/SpO2/sleep need via DailySleepData."""
    fixture = {
        "sleeping_seconds": 25200,
        "sleep_start_timestamp_gmt": 1788100000000,
        "average_sp_o2_value": 96,
    }

    with patch("garth.data.DailySleepData.get", return_value=MagicMock()) as mock_get:
        with patch("mcp_garmin.client.asdict", return_value=fixture):
            result = get_sleep_summary(day="2026-08-31")

    mock_get.assert_called_once()
    assert mock_get.call_args.kwargs["day"] == "2026-08-31"
    assert result == fixture


def test_get_sleep_summary_none():
    """Sleep summary handles None."""
    with patch("garth.data.DailySleepData.get", return_value=None):
        result = get_sleep_summary(day="2026-08-31")

    assert result == {}
