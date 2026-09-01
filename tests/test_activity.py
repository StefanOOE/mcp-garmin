"""Tests for mcp_garmin.activity."""
from __future__ import annotations

from unittest.mock import MagicMock, patch


def _patch_client(monkeypatch, mock_client):
    import mcp_garmin.activity as activity

    monkeypatch.setattr(activity, "get_client", lambda: mock_client)


def test_get_activities(monkeypatch):
    import mcp_garmin.activity as activity_mod

    fixture = {"activity_id": 123, "type_id": 9}
    _patch_client(monkeypatch, MagicMock())
    with patch("garth.data.Activity.list", return_value=[fixture]) as mock_list:
        result = activity_mod.get_activities(limit=20, start=0)
    mock_list.assert_called_once()
    assert mock_list.call_args.kwargs["limit"] == 20
    assert mock_list.call_args.kwargs["start"] == 0
    assert result == [fixture]


def test_get_activity_detail(monkeypatch):
    import mcp_garmin.activity as activity_mod

    fixture = {"activity_id": 123, "distance": 15000}
    _patch_client(monkeypatch, MagicMock())
    with patch("garth.data.Activity.get", return_value=fixture) as mock_get:
        result = activity_mod.get_activity_detail(activity_id=123)
    mock_get.assert_called_once()
    assert mock_get.call_args.kwargs["activity_id"] == 123
    assert result == fixture


def test_get_activity_map(monkeypatch):
    import mcp_garmin.activity as activity_mod

    fixture = {"map": {"lat": 48.2, "lon": 16.3}}
    _patch_client(monkeypatch, MagicMock())
    with patch("garth.data.Activity.map_details", return_value=fixture) as mock_map:
        result = activity_mod.get_activity_map(activity_id=123)
    mock_map.assert_called_once()
    assert mock_map.call_args.kwargs["activity_id"] == 123
    assert result == fixture


def test_get_fitness_activities(monkeypatch):
    import mcp_garmin.activity as activity_mod

    fixture = {"calendar_date": "2026-08-31", "total_steps": 20882}
    _patch_client(monkeypatch, MagicMock())
    with patch("garth.data.FitnessActivity.list", return_value=[fixture]) as mock_list:
        result = activity_mod.get_fitness_activities(end="2026-08-31", days=7)
    mock_list.assert_called_once()
    assert mock_list.call_args.kwargs["end"] == "2026-08-31"
    assert mock_list.call_args.kwargs["days"] == 7
    assert result == [fixture]


def test_get_personal_records(monkeypatch):
    import mcp_garmin.activity as activity_mod

    fixture = {"type_id": 12, "value": 5.5}
    _patch_client(monkeypatch, MagicMock())
    with patch("garth.data.PersonalRecord.list", return_value=[fixture]) as mock_list:
        result = activity_mod.get_personal_records()
    mock_list.assert_called_once()
    assert result == [fixture]


def test_get_personal_record_types(monkeypatch):
    import mcp_garmin.activity as activity_mod

    fixture = {"type_id": 12, "name": "FASTEST_TIME"}
    _patch_client(monkeypatch, MagicMock())
    with patch("garth.data.PersonalRecordType.list", return_value=[fixture]) as mock_list:
        result = activity_mod.get_personal_record_types()
    mock_list.assert_called_once()
    assert result == [fixture]
