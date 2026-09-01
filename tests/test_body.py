"""Tests for mcp_garmin.body."""
from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest


def _patch_client(monkeypatch, mock_client):
    import mcp_garmin.body as body

    monkeypatch.setattr(body, "get_client", lambda: mock_client)


def test_get_body_weight(monkeypatch, weight_fixture):
    from unittest.mock import patch

    import mcp_garmin.body as body

    _patch_client(monkeypatch, MagicMock())
    with patch("garth.data.WeightData.get", return_value=weight_fixture) as mock_get:
        result = body.get_body_weight(day="2026-09-01")
    mock_get.assert_called_once()
    assert mock_get.call_args.kwargs["day"] == "2026-09-01"
    assert mock_get.call_args.kwargs["client"] is not None
    assert result == weight_fixture


def test_get_weight_history(monkeypatch, weight_fixture):
    from unittest.mock import patch

    import mcp_garmin.body as body

    _patch_client(monkeypatch, MagicMock())
    with patch("garth.data.WeightData.list", return_value=[weight_fixture]) as mock_list:
        result = body.get_weight_history(end="2026-09-01", days=7)
    mock_list.assert_called_once()
    assert mock_list.call_args.kwargs["end"] == "2026-09-01"
    assert mock_list.call_args.kwargs["days"] == 7
    assert result == [weight_fixture]


def test_get_blood_pressure(monkeypatch):
    from unittest.mock import patch

    import mcp_garmin.body as body

    fixture = {"systolic_bp": 120, "diastolic_bp": 80, "calendar_date": "2026-09-01"}
    _patch_client(monkeypatch, MagicMock())
    with patch("garth.data.BloodPressure.get", return_value=fixture) as mock_get:
        result = body.get_blood_pressure(day="2026-09-01")
    mock_get.assert_called_once()
    assert mock_get.call_args.kwargs["day"] == "2026-09-01"
    assert result == fixture


def test_get_body_battery(monkeypatch):
    from unittest.mock import patch

    import mcp_garmin.body as body

    fixture = {"body_battery": 78, "calendar_date": "2026-09-01"}
    _patch_client(monkeypatch, MagicMock())
    with patch("garth.data.BodyBatteryData.get", return_value=[fixture]) as mock_get:
        result = body.get_body_battery(day="2026-09-01")
    mock_get.assert_called_once()
    assert mock_get.call_args.kwargs["day"] == "2026-09-01"
    assert result == [fixture]


def test_get_body_battery_stress(monkeypatch):
    from unittest.mock import patch

    import mcp_garmin.body as body

    fixture = {"stress_level": 23, "calendar_date": "2026-09-01"}
    _patch_client(monkeypatch, MagicMock())
    with patch(
        "garth.data.DailyBodyBatteryStress.get", return_value=fixture
    ) as mock_get:
        result = body.get_body_battery_stress(day="2026-09-01")
    mock_get.assert_called_once()
    assert mock_get.call_args.kwargs["day"] == "2026-09-01"
    assert result == fixture


def test_get_body_battery_stress_history(monkeypatch):
    from unittest.mock import patch

    import mcp_garmin.body as body

    fixture = {"stress_level": 23, "calendar_date": "2026-08-31"}
    _patch_client(monkeypatch, MagicMock())
    with patch(
        "garth.data.DailyBodyBatteryStress.list", return_value=[fixture]
    ) as mock_list:
        result = body.get_body_battery_stress_history(end="2026-09-01", days=7)
    mock_list.assert_called_once()
    assert mock_list.call_args.kwargs["end"] == "2026-09-01"
    assert mock_list.call_args.kwargs["days"] == 7
    assert result == [fixture]


def test_get_body_weight_raises_tool_error(monkeypatch):
    from garth.exc import GarthException

    import mcp_garmin.body as body
    from mcp_garmin.client import ToolError

    _patch_client(monkeypatch, MagicMock())
    with patch("garth.data.WeightData.get", side_effect=GarthException("token expired")):
        with pytest.raises(ToolError, match="garmin_login.py"):
            body.get_body_weight(day="2026-09-01")
