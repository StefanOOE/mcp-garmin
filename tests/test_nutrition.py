"""Tests für mcp_garmin.nutrition."""
from __future__ import annotations

from unittest.mock import patch


def _patch_client(monkeypatch, mock_client):
    import mcp_garmin.nutrition as nutrition

    monkeypatch.setattr(nutrition, "get_client", lambda: mock_client)


# --- get_nutrition_log ---


def test_get_nutrition_log(monkeypatch, mock_client):
    """NutritionLog.get liefert dict → _to_dict zurück."""
    import mcp_garmin.nutrition as nutrition

    fixture = {"total_calories": 2400, "total_protein": 150, "calendar_date": "2026-09-01"}
    _patch_client(monkeypatch, mock_client)

    with patch("garth.data.NutritionLog.get", return_value=fixture) as mock_get:
        result = nutrition.get_nutrition_log(day="2026-09-01")

    mock_get.assert_called_once()
    assert mock_get.call_args.kwargs["day"] == "2026-09-01"
    assert mock_get.call_args.kwargs["client"] is not None
    assert result == fixture


def test_get_nutrition_log_none(monkeypatch, mock_client):
    """NutritionLog.get liefert None → {} zurück."""
    import mcp_garmin.nutrition as nutrition

    _patch_client(monkeypatch, mock_client)

    with patch("garth.data.NutritionLog.get", return_value=None) as mock_get:
        result = nutrition.get_nutrition_log(day="2026-09-01")

    mock_get.assert_called_once()
    assert result == {}


def test_get_nutrition_log_no_day(monkeypatch, mock_client):
    """Ohne day-Parameter → day=None übergeben."""
    import mcp_garmin.nutrition as nutrition

    fixture = {"total_calories": 2000}
    _patch_client(monkeypatch, mock_client)

    with patch("garth.data.NutritionLog.get", return_value=fixture) as mock_get:
        result = nutrition.get_nutrition_log()

    mock_get.assert_called_once()
    assert mock_get.call_args.kwargs["day"] is None
    assert result == fixture


# --- get_nutrition_status ---


def test_get_nutrition_status(monkeypatch, mock_client):
    """NutritionStatus.get liefert dict → _to_dict zurück."""
    import mcp_garmin.nutrition as nutrition

    fixture = {"target_calories": 2500, "consumed_calories": 1200, "target_protein": 160}
    _patch_client(monkeypatch, mock_client)

    with patch("garth.data.NutritionStatus.get", return_value=fixture) as mock_get:
        result = nutrition.get_nutrition_status()

    mock_get.assert_called_once()
    assert result == fixture


def test_get_nutrition_status_none(monkeypatch, mock_client):
    """NutritionStatus.get liefert None → {} zurück."""
    import mcp_garmin.nutrition as nutrition

    _patch_client(monkeypatch, mock_client)

    with patch("garth.data.NutritionStatus.get", return_value=None) as mock_get:
        result = nutrition.get_nutrition_status()

    mock_get.assert_called_once()
    assert result == {}
