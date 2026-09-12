"""Unit tests for body tools."""
from __future__ import annotations

from unittest.mock import MagicMock, patch

from mcp_garmin.tools.body import get_body_weight, get_weight_history, get_blood_pressure, get_body_battery, get_body_battery_stress, get_body_battery_stress_history


def test_get_body_weight():
    """Body weight for a day (YYYY-MM-DD) — grams, BMI, body fat, etc."""
    fixture = {"weight": 75000, "bmi": 24.5, "body_fat": 18.2}
    mock_client = MagicMock()
    
    with patch("garth.data.WeightData.get", return_value=fixture) as mock_get:
        result = get_body_weight(day="2026-09-01")
    
    mock_get.assert_called_once()
    assert mock_get.call_args.kwargs["day"] == "2026-09-01"
    assert mock_get.call_args.kwargs["client"] is not None
    assert result == fixture


def test_get_weight_history():
    """Weight history for the last N days (up to end, YYYY-MM-DD)."""
    fixture = {"weight": 75000, "bmi": 24.5}
    mock_client = MagicMock()
    
    with patch(
        "garth.data.WeightData.list", return_value=[fixture]
    ) as mock_list:
        result = get_weight_history(end="2026-09-01", days=7)
    
    mock_list.assert_called_once()
    assert mock_list.call_args.kwargs["end"] == "2026-09-01"
    assert mock_list.call_args.kwargs["days"] == 7
    assert result == [fixture]


def test_get_blood_pressure(monkeypatch):
    """Blood pressure reading for a day (YYYY-MM-DD)."""
    fixture = {"systolicBp": 120, "diastolicBp": 80, "calendarDate": "2026-09-01"}
    expected = {"systolic_bp": 120, "diastolic_bp": 80, "calendar_date": "2026-09-01"}
    import mcp_garmin.tools.body as body

    mock_client = MagicMock()
    mock_client.connectapi.return_value = fixture
    monkeypatch.setattr(body, "get_client", lambda: mock_client)

    result = get_blood_pressure(day="2026-09-01")

    mock_client.connectapi.assert_called_once_with(
        "/bloodpressure-service/bloodpressure/dayview/2026-09-01"
    )
    assert result == expected


def test_get_body_battery():
    """Body Battery readings for a day (YYYY-MM-DD)."""
    fixture = {"body_battery": 78, "calendar_date": "2026-09-01"}
    mock_client = MagicMock()
    
    with patch("garth.data.BodyBatteryData.get", return_value=[fixture]) as mock_get:
        result = get_body_battery(day="2026-09-01")
    
    mock_get.assert_called_once()
    assert mock_get.call_args.kwargs["day"] == "2026-09-01"
    assert result == [fixture]


def test_get_body_battery_stress():
    """Body Battery + stress summary for a day (YYYY-MM-DD)."""
    fixture = {"stress_level": 23, "calendar_date": "2026-09-01"}
    mock_client = MagicMock()
    
    with patch(
        "garth.data.DailyBodyBatteryStress.get", return_value=fixture
    ) as mock_get:
        result = get_body_battery_stress(day="2026-09-01")
    
    mock_get.assert_called_once()
    assert mock_get.call_args.kwargs["day"] == "2026-09-01"
    assert result == fixture


def test_get_body_battery_stress_history():
    """Body Battery + stress history for the last N days (up to end)."""
    fixture = {"stress_level": 23, "calendar_date": "2026-08-31"}
    mock_client = MagicMock()
    
    with patch(
        "garth.data.DailyBodyBatteryStress.list", return_value=[fixture]
    ) as mock_list:
        result = get_body_battery_stress_history(end="2026-09-01", days=7)
    
    mock_list.assert_called_once()
    assert mock_list.call_args.kwargs["end"] == "2026-09-01"
    assert mock_list.call_args.kwargs["days"] == 7
    assert result == [fixture]