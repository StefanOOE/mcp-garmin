"""Unit tests for hydration tools."""
from __future__ import annotations

from unittest.mock import MagicMock, patch

from mcp_garmin.tools.hydration import get_daily_hydration, get_hydration_history


def test_get_daily_hydration():
    """list(end=day, period=1) → per-day entry [0] serialized."""
    fixture = MagicMock()
    fixture_dict = {
        "calendar_date": "2026-09-01",
        "value_in_ml": 1500.0,
        "goal_in_ml": 3000.0,
    }
    mock_client = MagicMock()
    
    with (
        patch("garth.stats.DailyHydration.list", return_value=[fixture]) as mock_list,
        patch("mcp_garmin.client.asdict", return_value=fixture_dict),
    ):
        result = get_daily_hydration(day="2026-09-01")
    
    mock_list.assert_called_once()
    assert mock_list.call_args.kwargs["end"] == "2026-09-01"
    assert mock_list.call_args.kwargs["period"] == 1
    assert result == fixture_dict


def test_get_daily_hydration_empty():
    """list() → [] (no data for the day) → {} (dict contract preserved)."""
    mock_client = MagicMock()
    
    with patch("garth.stats.DailyHydration.list", return_value=[]):
        result = get_daily_hydration(day="2026-09-01")
    
    assert result == {}


def test_get_hydration_history():
    """list(end=end, period=days) — days param maps to period."""
    fixture = MagicMock()
    fixture_dict = {
        "calendar_date": "2026-08-31",
        "value_in_ml": 2200.0,
        "goal_in_ml": 3000.0,
    }
    mock_client = MagicMock()
    
    with (
        patch("garth.stats.DailyHydration.list", return_value=[fixture]) as mock_list,
        patch("mcp_garmin.client.asdict", return_value=fixture_dict),
    ):
        result = get_hydration_history(end="2026-08-31", days=1)
    
    mock_list.assert_called_once()
    assert mock_list.call_args.kwargs["end"] == "2026-08-31"
    assert mock_list.call_args.kwargs["period"] == 1
    assert result == [fixture_dict]