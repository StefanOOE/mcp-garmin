"""Unit tests for steps tools."""
from __future__ import annotations

from unittest.mock import MagicMock, patch

from mcp_garmin.tools.steps import (
    get_daily_steps,
    get_weekly_steps,
    get_daily_summary,
    get_daily_summary_history,
)


def test_get_daily_steps():
    """Daily steps data for a day (YYYY-MM-DD)."""
    fixture = {"steps": 10000, "calendar_date": "2026-08-31"}

    with patch("garth.stats.DailySteps.list", return_value=[fixture]) as mock_list:
        with patch("mcp_garmin.client.asdict", return_value=fixture):
            result = get_daily_steps(day="2026-08-31")

    mock_list.assert_called_once()
    assert mock_list.call_args.kwargs["end"] == "2026-08-31"
    assert mock_list.call_args.kwargs["period"] == 1
    assert result == fixture


def test_get_weekly_steps():
    """Weekly steps data starting from a date (YYYY-MM-DD)."""
    fixture = {"steps": 10000, "calendar_date": "2026-08-31"}

    with patch("garth.stats.WeeklySteps.list", return_value=[fixture]) as mock_list:
        with patch("mcp_garmin.client.asdict", return_value=fixture):
            result = get_weekly_steps(end="2026-08-31", period=1)

    mock_list.assert_called_once()
    assert mock_list.call_args.kwargs["end"] == "2026-08-31"
    assert mock_list.call_args.kwargs["period"] == 1
    assert result == [fixture]


def test_get_daily_summary():
    """Daily summary for a day (YYYY-MM-DD)."""
    fixture = {"steps": 10000, "calendar_date": "2026-08-31"}
    mock_client = MagicMock()

    with patch("garth.data.DailySummary.get", return_value=fixture) as mock_get:
        with patch("mcp_garmin.client.asdict", return_value=fixture):
            result = get_daily_summary(day="2026-08-31")

    mock_get.assert_called_once()
    assert mock_get.call_args.kwargs["day"] == "2026-08-31"
    assert result == fixture


def test_get_daily_summary_history():
    """Daily summary history for the last N days (up to end)."""
    fixture = {"steps": 10000, "calendar_date": "2026-08-31"}

    with patch("garth.data.DailySummary.list", return_value=[fixture]) as mock_list:
        with patch("mcp_garmin.client.asdict", return_value=fixture):
            result = get_daily_summary_history(end="2026-08-31", days=7)

    mock_list.assert_called_once()
    assert mock_list.call_args.kwargs["end"] == "2026-08-31"
    assert mock_list.call_args.kwargs["days"] == 7
    assert result == [fixture]
