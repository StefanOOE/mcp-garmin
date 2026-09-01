"""Tests für mcp_garmin.steps."""
from __future__ import annotations

from unittest.mock import MagicMock, patch


def _patch_client(monkeypatch, mock_client):
    import mcp_garmin.steps as steps

    monkeypatch.setattr(steps, "get_client", lambda: mock_client)


def test_get_daily_steps(monkeypatch, daily_steps_fixture):
    import mcp_garmin.steps as steps_mod

    _patch_client(monkeypatch, MagicMock())
    with patch("garth.DailySteps.list", return_value=[daily_steps_fixture]) as mock_list:
        result = steps_mod.get_daily_steps(end="2026-08-31")
    mock_list.assert_called_once()
    assert mock_list.call_args.kwargs["end"] == "2026-08-31"
    assert mock_list.call_args.kwargs["period"] == 1
    assert result == [daily_steps_fixture]


def test_get_weekly_steps(monkeypatch, daily_steps_fixture):
    import mcp_garmin.steps as steps_mod

    _patch_client(monkeypatch, MagicMock())
    with patch("garth.DailySteps.list", return_value=[daily_steps_fixture]) as mock_list:
        result = steps_mod.get_weekly_steps(end="2026-08-31")
    mock_list.assert_called_once()
    assert mock_list.call_args.kwargs["end"] == "2026-08-31"
    assert mock_list.call_args.kwargs["period"] == 7
    assert result == [daily_steps_fixture]


def test_get_daily_summary(monkeypatch, daily_summary_fixture):
    import mcp_garmin.steps as steps_mod

    _patch_client(monkeypatch, MagicMock())
    with patch("garth.data.DailySummary.get", return_value=daily_summary_fixture) as mock_get:
        result = steps_mod.get_daily_summary(day="2026-08-31")
    mock_get.assert_called_once()
    assert mock_get.call_args.kwargs["day"] == "2026-08-31"
    assert result == daily_summary_fixture


def test_get_daily_summary_history(monkeypatch, daily_summary_fixture):
    import mcp_garmin.steps as steps_mod

    _patch_client(monkeypatch, MagicMock())
    with patch("garth.data.DailySummary.list", return_value=[daily_summary_fixture]) as mock_list:
        result = steps_mod.get_daily_summary_history(end="2026-08-31", days=7)
    mock_list.assert_called_once()
    assert mock_list.call_args.kwargs["end"] == "2026-08-31"
    assert mock_list.call_args.kwargs["days"] == 7
    assert result == [daily_summary_fixture]
