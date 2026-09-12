"""Unit tests for activity tools."""
from __future__ import annotations

from unittest.mock import MagicMock, patch

from mcp_garmin.tools.activity import (
    get_activities,
    get_activity_detail,
    get_activity_map,
    get_fitness_activities,
    get_personal_records,
    get_personal_record_types,
)


def _patch_client(monkeypatch, mock_client):
    import mcp_garmin.tools.activity as activity

    monkeypatch.setattr(activity, "get_client", lambda: mock_client)


def test_get_activities(monkeypatch):
    """Activity.list(limit, start) — no end/days."""
    fixture = MagicMock()
    fixture_dict = {"activity_id": 123, "type_id": 9}
    _patch_client(monkeypatch, MagicMock())

    with (
        patch("garth.data.Activity.list", return_value=[fixture]) as mock_list,
        patch("mcp_garmin.client.asdict", return_value=fixture_dict),
    ):
        result = get_activities(limit=20, start=0)

    mock_list.assert_called_once()
    assert mock_list.call_args.kwargs["limit"] == 20
    assert mock_list.call_args.kwargs["start"] == 0
    assert result == [fixture_dict]


def test_get_activities_custom_pagination(monkeypatch):
    """limit/start are forwarded 1:1 (breaking pagination contract)."""
    _patch_client(monkeypatch, MagicMock())

    with (
        patch("garth.data.Activity.list", return_value=[]) as mock_list,
        patch("mcp_garmin.client.asdict"),
    ):
        get_activities(limit=10, start=40)

    assert mock_list.call_args.kwargs["limit"] == 10
    assert mock_list.call_args.kwargs["start"] == 40


def test_get_activity_detail(monkeypatch):
    """Activity.get(activity_id)."""
    fixture = MagicMock()
    fixture_dict = {"activity_id": 123, "distance": 15000}
    _patch_client(monkeypatch, MagicMock())

    with (
        patch("garth.data.Activity.get", return_value=fixture) as mock_get,
        patch("mcp_garmin.client.asdict", return_value=fixture_dict),
    ):
        result = get_activity_detail(activity_id=123)

    mock_get.assert_called_once()
    assert mock_get.call_args.kwargs["activity_id"] == 123
    assert result == fixture_dict


def test_get_activity_map(monkeypatch):
    """connectapi path (no /proxy prefix) + both payload keys, snake_cased."""
    fixture = {
        "activityHeatMapDTO": {"heatmapType": "INTENSITY", "intensityRange": 300},
        "gPolyline": "a]F~FzF~FzF",
    }
    mock_client = MagicMock()
    mock_client.connectapi.return_value = fixture
    _patch_client(monkeypatch, mock_client)

    result = get_activity_map(activity_id=123)

    mock_client.connectapi.assert_called_once_with(
        "/activity-service/activity/123/mapdetails"
    )
    assert result == {
        "activity_heat_map_dto": {
            "heatmap_type": "INTENSITY",
            "intensity_range": 300,
        },
        "g_polyline": "a]F~FzF~FzF",
    }


def test_get_activity_map_none(monkeypatch):
    """connectapi returns None (204) → {} (dict contract preserved)."""
    mock_client = MagicMock()
    mock_client.connectapi.return_value = None
    _patch_client(monkeypatch, mock_client)

    result = get_activity_map(activity_id=123)

    mock_client.connectapi.assert_called_once_with(
        "/activity-service/activity/123/mapdetails"
    )
    assert result == {}


def test_get_fitness_activities(monkeypatch):
    """FitnessActivity.list(end, days)."""
    fixture = MagicMock()
    fixture_dict = {"calendar_date": "2026-08-31", "total_steps": 20882}
    _patch_client(monkeypatch, MagicMock())

    with (
        patch("garth.data.FitnessActivity.list", return_value=[fixture]) as mock_list,
        patch("mcp_garmin.client.asdict", return_value=fixture_dict),
    ):
        result = get_fitness_activities(end="2026-08-31", days=7)

    mock_list.assert_called_once()
    assert mock_list.call_args.kwargs["end"] == "2026-08-31"
    assert mock_list.call_args.kwargs["days"] == 7
    assert result == [fixture_dict]


def test_get_personal_records(monkeypatch):
    """connectapi PR list → per-entry camel_to_snake_dict."""
    fixture = [
        {"typeId": 12, "value": 5.5},
        {"typeId": 13, "value": 10.2},
    ]
    mock_client = MagicMock()
    mock_client.connectapi.return_value = fixture
    _patch_client(monkeypatch, mock_client)

    result = get_personal_records()

    mock_client.connectapi.assert_called_once_with(
        "/personalrecord-service/personalrecord"
    )
    assert result == [
        {"type_id": 12, "value": 5.5},
        {"type_id": 13, "value": 10.2},
    ]


def test_get_personal_records_none(monkeypatch):
    """connectapi returns None → [] (list contract preserved)."""
    mock_client = MagicMock()
    mock_client.connectapi.return_value = None
    _patch_client(monkeypatch, mock_client)

    result = get_personal_records()

    assert result == []


def test_get_personal_record_types(monkeypatch):
    """connectapi PR-type list → per-entry camel_to_snake_dict."""
    fixture = [
        {"typeId": 12, "typeName": "FASTEST_TIME", "unit": "SECONDS"},
    ]
    mock_client = MagicMock()
    mock_client.connectapi.return_value = fixture
    _patch_client(monkeypatch, mock_client)

    result = get_personal_record_types()

    mock_client.connectapi.assert_called_once_with(
        "/personalrecord-service/personalrecordtype"
    )
    assert result == [
        {"type_id": 12, "type_name": "FASTEST_TIME", "unit": "SECONDS"},
    ]


def test_get_personal_record_types_none(monkeypatch):
    """connectapi returns None → [] (list contract preserved)."""
    mock_client = MagicMock()
    mock_client.connectapi.return_value = None
    _patch_client(monkeypatch, mock_client)

    result = get_personal_record_types()

    assert result == []
