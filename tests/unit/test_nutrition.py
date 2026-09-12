"""Unit tests for nutrition tools."""
from __future__ import annotations

from datetime import date
from unittest.mock import MagicMock, patch

from mcp_garmin.tools.nutrition import get_nutrition_log, get_nutrition_status


def test_get_nutrition_log():
    """connectapi returns a day-log dict → camelCase is converted to snake_case."""
    fixture = {
        "mealDate": "2026-09-01",
        "dayStartTime": 1788153326000,
        "dailyNutritionGoals": {"calories": 2500, "protein": 160},
        "mealDetails": [{"foodName": "Coffee", "calories": 5}],
    }
    mock_client = MagicMock()
    mock_client.connectapi.return_value = fixture
    
    result = get_nutrition_log(day="2026-09-01")
    
    mock_client.connectapi.assert_called_once_with(
        "/nutrition-service/food/logs/2026-09-01"
    )
    assert result == {
        "meal_date": "2026-09-01",
        "day_start_time": 1788153326000,
        "daily_nutrition_goals": {"calories": 2500, "protein": 160},
        "meal_details": [{"food_name": "Coffee", "calories": 5}],
    }


def test_get_nutrition_log_defaults_to_today():
    """Ohne day-Parameter → heute (ISO) wird im Pfad verwendet."""
    mock_client = MagicMock()
    mock_client.connectapi.return_value = {"mealDate": date.today().isoformat()}
    
    result = get_nutrition_log()
    
    expected_path = f"/nutrition-service/food/logs/{date.today().isoformat()}"
    mock_client.connectapi.assert_called_once_with(expected_path)
    assert result == {"meal_date": date.today().isoformat()}


def test_get_nutrition_log_none():
    """connectapi liefert None → {} zurück."""
    mock_client = MagicMock()
    mock_client.connectapi.return_value = None
    
    result = get_nutrition_log(day="2026-09-01")
    
    mock_client.connectapi.assert_called_once_with(
        "/nutrition-service/food/logs/2026-09-01"
    )
    assert result == {}


def test_get_nutrition_log_empty_dict():
    """connectapi liefert leeres Dict → {} zurück."""
    mock_client = MagicMock()
    mock_client.connectapi.return_value = {}
    
    result = get_nutrition_log(day="2026-09-01")
    
    assert result == {}


def test_get_nutrition_status():
    """connectapi returns the current status dict → snake_case, no day param."""
    fixture = {
        "currentStatus": "MFP_ENABLED",
        "hasUsedNutrition": False,
        "hasUsedMFP": True,
    }
    mock_client = MagicMock()
    mock_client.connectapi.return_value = fixture
    
    result = get_nutrition_status()
    
    # No day parameter — always the current-status endpoint.
    mock_client.connectapi.assert_called_once_with(
        "/nutrition-service/user/nutritionCurrentStatus"
    )
    assert result == {
        "current_status": "MFP_ENABLED",
        "has_used_nutrition": False,
        "has_used_mfp": True,
    }


def test_get_nutrition_status_none():
    """connectapi returns None → {} returned."""
    mock_client = MagicMock()
    mock_client.connectapi.return_value = None
    
    result = get_nutrition_status()
    
    mock_client.connectapi.assert_called_once_with(
        "/nutrition-service/user/nutritionCurrentStatus"
    )
    assert result == {}