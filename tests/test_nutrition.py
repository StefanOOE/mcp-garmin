"""Tests for mcp_garmin.nutrition (garth-ng 1.1.0 Endpoint-Fallback).

Both tools use ``client.connectapi(path)`` + ``camel_to_snake_dict()``
(S1 §1.7). These tests assert the exact path contract:
* log    -- ``/nutrition-service/food/logs/{day}`` (day defaults to today).
* status -- ``/nutrition-service/user/nutritionCurrentStatus`` (no day).
"""

from __future__ import annotations

from datetime import date


def _patch_client(monkeypatch, mock_client):
    import mcp_garmin.nutrition as nutrition

    monkeypatch.setattr(nutrition, "get_client", lambda: mock_client)


# --- get_nutrition_log ---


def test_get_nutrition_log(monkeypatch, mock_client):
    """connectapi returns a day-log dict → camelCase is converted to snake_case."""
    import mcp_garmin.nutrition as nutrition

    fixture = {
        "mealDate": "2026-09-01",
        "dayStartTime": 1788153326000,
        "dailyNutritionGoals": {"calories": 2500, "protein": 160},
        "mealDetails": [{"foodName": "Coffee", "calories": 5}],
    }
    mock_client.connectapi.return_value = fixture
    _patch_client(monkeypatch, mock_client)

    result = nutrition.get_nutrition_log(day="2026-09-01")

    mock_client.connectapi.assert_called_once_with(
        "/nutrition-service/food/logs/2026-09-01"
    )
    assert result == {
        "meal_date": "2026-09-01",
        "day_start_time": 1788153326000,
        "daily_nutrition_goals": {"calories": 2500, "protein": 160},
        "meal_details": [{"food_name": "Coffee", "calories": 5}],
    }


def test_get_nutrition_log_defaults_to_today(monkeypatch, mock_client):
    """Ohne day-Parameter → heute (ISO) wird im Pfad verwendet."""
    import mcp_garmin.nutrition as nutrition

    mock_client.connectapi.return_value = {"mealDate": date.today().isoformat()}
    _patch_client(monkeypatch, mock_client)

    result = nutrition.get_nutrition_log()

    expected_path = f"/nutrition-service/food/logs/{date.today().isoformat()}"
    mock_client.connectapi.assert_called_once_with(expected_path)
    assert result == {"meal_date": date.today().isoformat()}


def test_get_nutrition_log_none(monkeypatch, mock_client):
    """connectapi liefert None → {} zurück."""
    import mcp_garmin.nutrition as nutrition

    mock_client.connectapi.return_value = None
    _patch_client(monkeypatch, mock_client)

    result = nutrition.get_nutrition_log(day="2026-09-01")

    mock_client.connectapi.assert_called_once_with(
        "/nutrition-service/food/logs/2026-09-01"
    )
    assert result == {}


def test_get_nutrition_log_empty_dict(monkeypatch, mock_client):
    """connectapi liefert leeres Dict → {} zurück."""
    import mcp_garmin.nutrition as nutrition

    mock_client.connectapi.return_value = {}
    _patch_client(monkeypatch, mock_client)

    result = nutrition.get_nutrition_log(day="2026-09-01")

    assert result == {}


# --- get_nutrition_status ---


def test_get_nutrition_status(monkeypatch, mock_client):
    """connectapi returns the current status dict → snake_case, no day param."""
    import mcp_garmin.nutrition as nutrition

    fixture = {
        "currentStatus": "MFP_ENABLED",
        "hasUsedNutrition": False,
        "hasUsedMFP": True,
    }
    mock_client.connectapi.return_value = fixture
    _patch_client(monkeypatch, mock_client)

    result = nutrition.get_nutrition_status()

    # No day parameter — always the current-status endpoint.
    mock_client.connectapi.assert_called_once_with(
        "/nutrition-service/user/nutritionCurrentStatus"
    )
    assert result == {
        "current_status": "MFP_ENABLED",
        "has_used_nutrition": False,
        "has_used_mfp": True,
    }


def test_get_nutrition_status_none(monkeypatch, mock_client):
    """connectapi returns None → {} returned."""
    import mcp_garmin.nutrition as nutrition

    mock_client.connectapi.return_value = None
    _patch_client(monkeypatch, mock_client)

    result = nutrition.get_nutrition_status()

    mock_client.connectapi.assert_called_once_with(
        "/nutrition-service/user/nutritionCurrentStatus"
    )
    assert result == {}
