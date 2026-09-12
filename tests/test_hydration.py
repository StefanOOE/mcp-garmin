"""Tests for hydration tools (garth-ng 1.1.0, S1 §1.6).

Both modules (``mcp_garmin.hydration`` root and ``mcp_garmin.tools.hydration``)
use ``garth.DailyHydration.list(end=..., period=..., client=...)`` — the
legacy ``HydrationData.get`` / ``all_data`` surface no longer exists. These
tests assert the exact remap contract:

* daily  -- ``list(end=day, period=1)`` + per-day entry extraction (``[0]``).
* history -- ``list(end=end, period=days)`` (``days`` → ``period``).
"""

from __future__ import annotations

from unittest.mock import MagicMock, patch


def _patch_client(monkeypatch, mock_client):
    import mcp_garmin.hydration as hydration

    monkeypatch.setattr(hydration, "get_client", lambda: mock_client)


# --- root module: mcp_garmin.hydration ---


def test_get_daily_hydration(monkeypatch):
    """list(end=day, period=1) → per-day entry [0] serialized."""
    import mcp_garmin.hydration as hydration_mod

    fixture = MagicMock()
    fixture_dict = {
        "calendar_date": "2026-09-01",
        "value_in_ml": 1500.0,
        "goal_in_ml": 3000.0,
    }
    mock_client = MagicMock()
    _patch_client(monkeypatch, mock_client)
    with (
        patch("garth.DailyHydration.list", return_value=[fixture]) as mock_list,
        patch("mcp_garmin.client.asdict", return_value=fixture_dict),
    ):
        result = hydration_mod.get_daily_hydration(day="2026-09-01")
    mock_list.assert_called_once()
    assert mock_list.call_args.kwargs["end"] == "2026-09-01"
    assert mock_list.call_args.kwargs["period"] == 1
    assert mock_list.call_args.kwargs["client"] is mock_client
    assert result == fixture_dict


def test_get_daily_hydration_empty(monkeypatch):
    """list() → [] (no data for the day) → {} (dict contract preserved)."""
    import mcp_garmin.hydration as hydration_mod

    _patch_client(monkeypatch, MagicMock())
    with patch("garth.DailyHydration.list", return_value=[]):
        result = hydration_mod.get_daily_hydration(day="2026-09-01")
    assert result == {}


def test_get_hydration_history(monkeypatch):
    """list(end=end, period=days) — days param maps to period."""
    import mcp_garmin.hydration as hydration_mod

    fixture = MagicMock()
    fixture_dict = {
        "calendar_date": "2026-08-31",
        "value_in_ml": 2200.0,
        "goal_in_ml": 3000.0,
    }
    mock_client = MagicMock()
    _patch_client(monkeypatch, mock_client)
    with (
        patch("garth.DailyHydration.list", return_value=[fixture]) as mock_list,
        patch("mcp_garmin.client.asdict", return_value=fixture_dict),
    ):
        result = hydration_mod.get_hydration_history(end="2026-08-31", days=1)
    mock_list.assert_called_once()
    assert mock_list.call_args.kwargs["end"] == "2026-08-31"
    assert mock_list.call_args.kwargs["period"] == 1
    assert mock_list.call_args.kwargs["client"] is mock_client
    assert result == [fixture_dict]


# --- tools module: mcp_garmin.tools.hydration (same contract, no divergence) ---


def test_tools_get_daily_hydration(monkeypatch):
    import mcp_garmin.tools.hydration as tools_hydration

    fixture = MagicMock()
    fixture_dict = {
        "calendar_date": "2026-09-01",
        "value_in_ml": 1800.0,
        "goal_in_ml": 3000.0,
    }
    mock_client = MagicMock()
    monkeypatch.setattr(tools_hydration, "get_client", lambda: mock_client)
    with (
        patch("garth.DailyHydration.list", return_value=[fixture]) as mock_list,
        patch("mcp_garmin.client.asdict", return_value=fixture_dict),
    ):
        result = tools_hydration.get_daily_hydration(day="2026-09-01")
    assert mock_list.call_args.kwargs["end"] == "2026-09-01"
    assert mock_list.call_args.kwargs["period"] == 1
    assert mock_list.call_args.kwargs["client"] is mock_client
    assert result == fixture_dict


def test_tools_get_hydration_history(monkeypatch):
    import mcp_garmin.tools.hydration as tools_hydration

    fixture = MagicMock()
    fixture_dict = {
        "calendar_date": "2026-08-31",
        "value_in_ml": 2100.0,
        "goal_in_ml": 3000.0,
    }
    mock_client = MagicMock()
    monkeypatch.setattr(tools_hydration, "get_client", lambda: mock_client)
    with (
        patch("garth.DailyHydration.list", return_value=[fixture]) as mock_list,
        patch("mcp_garmin.client.asdict", return_value=fixture_dict),
    ):
        result = tools_hydration.get_hydration_history(end="2026-08-31", days=7)
    assert mock_list.call_args.kwargs["end"] == "2026-08-31"
    assert mock_list.call_args.kwargs["period"] == 7
    assert mock_list.call_args.kwargs["client"] is mock_client
    assert result == [fixture_dict]
