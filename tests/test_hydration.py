"""Tests für mcp_garmin.hydration."""
from __future__ import annotations

from unittest.mock import MagicMock, patch


def _patch_client(monkeypatch, mock_client):
    import mcp_garmin.hydration as hydration

    monkeypatch.setattr(hydration, "get_client", lambda: mock_client)


def test_get_daily_hydration(monkeypatch):
    import mcp_garmin.hydration as hydration_mod

    fixture = {
        "calendar_date": "2026-09-01",
        "total_intake": 1500,
        "goal_intake": 3000,
    }
    _patch_client(monkeypatch, MagicMock())
    with patch("garth.DailyHydration.all_data", return_value=fixture) as mock_all:
        result = hydration_mod.get_daily_hydration(day="2026-09-01")
    mock_all.assert_called_once()
    assert mock_all.call_args.kwargs["day"] == "2026-09-01"
    assert result == fixture


def test_get_hydration_history(monkeypatch):
    import mcp_garmin.hydration as hydration_mod

    fixture = {"calendar_date": "2026-08-31", "total_intake": 2200}
    _patch_client(monkeypatch, MagicMock())
    with patch("garth.DailyHydration.list", return_value=[fixture]) as mock_list:
        result = hydration_mod.get_hydration_history(end="2026-08-31", days=1)
    mock_list.assert_called_once()
    assert mock_list.call_args.kwargs["end"] == "2026-08-31"
    assert mock_list.call_args.kwargs["period"] == 1
    assert result == [fixture]
