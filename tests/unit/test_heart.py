"""Unit tests for heart tools."""
from __future__ import annotations

from unittest.mock import MagicMock, patch

from mcp_garmin.tools.heart import (
    get_daily_heart_rate,
    get_hrv,
    get_resting_heart_rate,
)


def _patch_client(monkeypatch, mock_client):
    import mcp_garmin.tools.heart as heart
    
    monkeypatch.setattr(heart, "get_client", lambda: mock_client)


def test_get_daily_heart_rate(monkeypatch):
    """Daily heart rate data for a day (YYYY-MM-DD)."""
    fixture = {
        "max_heart_rate": 178,
        "min_heart_rate": 48,
        "calendar_date": "2026-09-01",
    }

    _patch_client(monkeypatch, MagicMock())
    with patch("garth.data.DailyHeartRate.get", return_value=fixture) as mock_get:
        result = get_daily_heart_rate(day="2026-09-01")

    mock_get.assert_called_once()
    assert mock_get.call_args.kwargs["day"] == "2026-09-01"
    assert result == fixture


def test_get_hrv(monkeypatch, daily_hrv_fixture):
    """HRV (Heart Rate Variability) data for a day (YYYY-MM-DD)."""
    _patch_client(monkeypatch, MagicMock())
    with patch(
        "garth.data.hrv.HRVData.list", return_value=[daily_hrv_fixture]
    ) as mock_list:
        result = get_hrv(end="2026-08-31", days=28)
    mock_list.assert_called_once()
    assert mock_list.call_args.kwargs["end"] == "2026-08-31"
    assert mock_list.call_args.kwargs["period"] == 28
    assert result == [daily_hrv_fixture]


def test_get_resting_heart_rate(monkeypatch):
    """Resting heart rate for a day (YYYY-MM-DD)."""
    fixture = {"resting_heart_rate": 52, "calendar_date": "2026-08-31"}
    
    _patch_client(monkeypatch, MagicMock())
    with patch("garth.data.DailyHeartRate.list", return_value=[fixture]) as mock_list:
        result = get_resting_heart_rate(end="2026-08-31", days=1)
    mock_list.assert_called_once()
    assert mock_list.call_args.kwargs["end"] == "2026-08-31"
    assert mock_list.call_args.kwargs["days"] == 1
    # Return only the essential fields as per B1 requirement
    expected = {
        "calendar_date": "2026-08-31",
        "resting_heart_rate": 52
    }
    assert result == expected


def test_get_hrv_default_period(monkeypatch, daily_hrv_fixture):
    """HRV with default period."""
    _patch_client(monkeypatch, MagicMock())
    with patch("garth.data.HRVData.get", return_value=[]) as mock_list:
        get_hrv()
    mock_list.assert_called_once()
    assert mock_list.call_args.kwargs["day"] is None