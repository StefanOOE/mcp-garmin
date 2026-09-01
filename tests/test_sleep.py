"""Tests für mcp_garmin.sleep."""
from __future__ import annotations

from unittest.mock import MagicMock, patch


def _patch_client(monkeypatch, mock_client):
    import mcp_garmin.sleep as sleep

    monkeypatch.setattr(sleep, "get_client", lambda: mock_client)


def test_get_sleep(monkeypatch):
    import mcp_garmin.sleep as sleep_mod

    fixture = {"sleep_time_seconds": 25200, "calendar_date": "2026-09-01"}
    _patch_client(monkeypatch, MagicMock())
    with patch("garth.SleepData.get", return_value=fixture) as mock_get:
        result = sleep_mod.get_sleep(day="2026-09-01")
    mock_get.assert_called_once()
    assert mock_get.call_args.kwargs["day"] == "2026-09-01"
    assert result == fixture


def test_get_sleep_detail(monkeypatch):
    import mcp_garmin.sleep as sleep_mod

    fixture = {"sleep_start_timestamp_gmt": 1788100000000, "sleep_end_timestamp_gmt": 1788190000000}
    _patch_client(monkeypatch, MagicMock())
    with patch("garth.data.DailySleepData.get", return_value=fixture) as mock_get:
        result = sleep_mod.get_sleep_detail(day="2026-09-01")
    mock_get.assert_called_once()
    assert mock_get.call_args.kwargs["day"] == "2026-09-01"
    assert result == fixture


def test_get_sleep_summary_extracts_sleep_fields(monkeypatch):
    import mcp_garmin.sleep as sleep_mod

    full = {
        "calendar_date": "2026-08-31",
        "total_steps": 20882,
        "resting_heart_rate": 52,
        "sleeping_seconds": 25200,
        "sleep_start_timestamp_gmt": 1788100000000,
    }
    _patch_client(monkeypatch, MagicMock())
    with patch("garth.data.DailySummary.get", return_value=full) as mock_get:
        result = sleep_mod.get_sleep_summary(day="2026-08-31")
    mock_get.assert_called_once()
    assert result == {
        "sleeping_seconds": 25200,
        "sleep_start_timestamp_gmt": 1788100000000,
    }


def test_get_sleep_summary_returns_full_when_no_sleep_fields(monkeypatch):
    import mcp_garmin.sleep as sleep_mod

    full = {"calendar_date": "2026-08-31", "total_steps": 20882}
    _patch_client(monkeypatch, MagicMock())
    with patch("garth.data.DailySummary.get", return_value=full):
        result = sleep_mod.get_sleep_summary(day="2026-08-31")
    assert result == full


def test_get_sleep_summary_none(monkeypatch):
    import mcp_garmin.sleep as sleep_mod

    _patch_client(monkeypatch, MagicMock())
    with patch("garth.data.DailySummary.get", return_value=None):
        result = sleep_mod.get_sleep_summary(day="2026-08-31")
    assert result == {}
