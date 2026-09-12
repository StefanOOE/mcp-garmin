"""Unit tests for heart tools."""
from __future__ import annotations

from unittest.mock import MagicMock, patch

from mcp_garmin.tools.heart import (
    get_daily_heart_rate,
    get_hrv,
    get_resting_heart_rate,
)


def test_get_daily_heart_rate():
    """Daily heart rate data for a day (YYYY-MM-DD)."""
    fixture = {
        "max_heart_rate": 178,
        "min_heart_rate": 48,
        "calendar_date": "2026-09-01",
    }

    with patch("garth.data.DailyHeartRate.get", return_value=fixture) as mock_get:
        with patch("mcp_garmin.client.asdict", return_value=fixture):
            result = get_daily_heart_rate(day="2026-09-01")

    mock_get.assert_called_once()
    assert mock_get.call_args.kwargs["day"] == "2026-09-01"
    assert result == fixture


def test_get_hrv():
    """HRV (Heart Rate Variability) data for a day (YYYY-MM-DD)."""
    fixture = {"hrv": 65, "calendar_date": "2026-08-31"}

    with patch("garth.data.HRVData.list", return_value=[fixture]) as mock_list:
        with patch("mcp_garmin.client.asdict", return_value=fixture):
            result = get_hrv(end="2026-08-31", days=28)

    mock_list.assert_called_once()
    assert mock_list.call_args.kwargs["end"] == "2026-08-31"
    assert mock_list.call_args.kwargs["days"] == 28
    assert result == [fixture]


def test_get_resting_heart_rate():
    """Resting heart rate for a day (YYYY-MM-DD)."""
    fixture = {"resting_heart_rate": 52, "calendar_date": "2026-08-31"}

    with patch("garth.data.DailyHeartRate.list", return_value=[fixture]) as mock_list:
        with patch("mcp_garmin.client.asdict", return_value=fixture):
            result = get_resting_heart_rate(end="2026-08-31", days=1)

    mock_list.assert_called_once()
    assert mock_list.call_args.kwargs["end"] == "2026-08-31"
    assert mock_list.call_args.kwargs["days"] == 1
    assert result == [fixture]


def test_get_hrv_default_period():
    """HRV with default period."""
    with patch("garth.data.HRVData.list", return_value=[]) as mock_list:
        get_hrv()

    mock_list.assert_called_once()
    assert mock_list.call_args.kwargs["days"] == 28
