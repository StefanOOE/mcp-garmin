"""Tests for mcp_garmin.stress."""
from __future__ import annotations

from unittest.mock import MagicMock, patch


def _patch_client(monkeypatch, mock_client):
    import mcp_garmin.stress as stress

    monkeypatch.setattr(stress, "get_client", lambda: mock_client)


def test_get_daily_stress(monkeypatch, daily_stress_fixture):
    import mcp_garmin.stress as stress_mod

    _patch_client(monkeypatch, MagicMock())
    with patch("garth.DailyStress.list", return_value=[daily_stress_fixture]) as mock_list:
        result = stress_mod.get_daily_stress(end="2026-08-31", days=1)
    mock_list.assert_called_once()
    assert mock_list.call_args.kwargs["end"] == "2026-08-31"
    assert mock_list.call_args.kwargs["period"] == 1
    assert result == [daily_stress_fixture]


def test_get_weekly_stress(monkeypatch, daily_stress_fixture):
    import mcp_garmin.stress as stress_mod

    _patch_client(monkeypatch, MagicMock())
    with patch("garth.DailyStress.list", return_value=[daily_stress_fixture]) as mock_list:
        result = stress_mod.get_weekly_stress(end="2026-08-31")
    mock_list.assert_called_once()
    assert mock_list.call_args.kwargs["end"] == "2026-08-31"
    assert mock_list.call_args.kwargs["period"] == 7
    assert result == [daily_stress_fixture]


def test_get_training_status_daily(monkeypatch):
    import mcp_garmin.stress as stress_mod

    fixture = {"training_readiness_score": 72, "calendar_date": "2026-09-01"}
    _patch_client(monkeypatch, MagicMock())
    with patch("garth.data.TrainingReadinessData.get", return_value=[fixture]) as mock_get:
        result = stress_mod.get_training_status_daily(day="2026-09-01")
    mock_get.assert_called_once()
    assert mock_get.call_args.kwargs["day"] == "2026-09-01"
    assert result == [fixture]


def test_get_training_status_weekly(monkeypatch):
    import mcp_garmin.stress as stress_mod

    fixture = {"training_readiness_score": 70}
    _patch_client(monkeypatch, MagicMock())
    with patch("garth.data.TrainingReadinessData.get", return_value=[fixture]) as mock_get:
        result = stress_mod.get_training_status_weekly(end="2026-09-01")
    mock_get.assert_called_once()
    assert mock_get.call_args.kwargs["day"] == "2026-09-01"
    assert result == [fixture]


def test_get_training_status_monthly(monkeypatch):
    import mcp_garmin.stress as stress_mod

    fixture = {"training_readiness_score": 65}
    _patch_client(monkeypatch, MagicMock())
    with patch("garth.data.TrainingReadinessData.get", return_value=[fixture]) as mock_get:
        result = stress_mod.get_training_status_monthly(end="2026-09-01")
    mock_get.assert_called_once()
    assert mock_get.call_args.kwargs["day"] == "2026-09-01"
    assert result == [fixture]


def test_get_training_status_none_returns_empty_list(monkeypatch):
    import mcp_garmin.stress as stress_mod

    _patch_client(monkeypatch, MagicMock())
    with patch("garth.data.TrainingReadinessData.get", return_value=None):
        assert stress_mod.get_training_status_daily(day="2026-09-01") == []


def test_get_training_readiness(monkeypatch):
    import mcp_garmin.stress as stress_mod

    fixture = {"training_readiness_score": 72, "calendar_date": "2026-09-01"}
    _patch_client(monkeypatch, MagicMock())
    with patch(
        "garth.data.MorningTrainingReadinessData.get", return_value=fixture
    ) as mock_get:
        result = stress_mod.get_training_readiness(day="2026-09-01")
    mock_get.assert_called_once()
    assert mock_get.call_args.kwargs["day"] == "2026-09-01"
    assert result == fixture


def test_get_morning_readiness_is_alias(monkeypatch):
    import mcp_garmin.stress as stress_mod

    fixture = {"training_readiness_score": 72}
    _patch_client(monkeypatch, MagicMock())
    with patch("garth.data.MorningTrainingReadinessData.get", return_value=fixture) as mock_get:
        result = stress_mod.get_morning_readiness(day="2026-09-01")
    mock_get.assert_called_once()
    assert mock_get.call_args.kwargs["day"] == "2026-09-01"
    assert result == fixture
