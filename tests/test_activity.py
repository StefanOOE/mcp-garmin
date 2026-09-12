"""Tests for mcp_garmin.activity (garth-ng 1.1.0, S1 §1.1).

Both modules (``mcp_garmin.activity`` root and ``mcp_garmin.tools.activity``)
implement the same contract — no divergence:

* activities -- ``garth.data.Activity.list(limit=..., start=..., client=...)``
  (breaking: no ``end``/``days``).
* detail     -- ``garth.data.Activity.get(activity_id=..., client=...)``.
* map        -- Endpoint-Fallback ``client.connectapi(...)`` +
  ``camel_to_snake_dict()`` (no accessor in 1.1.0). Path carries **no**
  ``/proxy`` prefix. Payload keys ``activityHeatMapDTO`` + ``gPolyline``.
* fitness    -- ``garth.data.FitnessActivity.list(end=..., days=..., client=...)``.
* PRs / PR types -- Endpoint-Fallback
  (``/personalrecord-service/personalrecord[``+``type]``).
"""

from __future__ import annotations

from unittest.mock import MagicMock, patch

# --- root module: mcp_garmin.activity ---


def _patch_client(monkeypatch, mock_client):
    import mcp_garmin.activity as activity

    monkeypatch.setattr(activity, "get_client", lambda: mock_client)


def test_get_activities(monkeypatch):
    """Activity.list(limit, start) — no end/days; client passed through."""
    import mcp_garmin.activity as activity_mod

    fixture = MagicMock()
    fixture_dict = {"activity_id": 123, "type_id": 9}
    mock_client = MagicMock()
    _patch_client(monkeypatch, mock_client)
    with (
        patch("garth.data.Activity.list", return_value=[fixture]) as mock_list,
        patch("mcp_garmin.client.asdict", return_value=fixture_dict),
    ):
        result = activity_mod.get_activities(limit=20, start=0)
    mock_list.assert_called_once()
    assert mock_list.call_args.kwargs["limit"] == 20
    assert mock_list.call_args.kwargs["start"] == 0
    assert mock_list.call_args.kwargs["client"] is mock_client
    assert result == [fixture_dict]


def test_get_activities_custom_pagination(monkeypatch):
    """limit/start are forwarded 1:1 (breaking pagination contract)."""
    import mcp_garmin.activity as activity_mod

    mock_client = MagicMock()
    _patch_client(monkeypatch, mock_client)
    with (
        patch("garth.data.Activity.list", return_value=[]) as mock_list,
        patch("mcp_garmin.client.asdict"),
    ):
        activity_mod.get_activities(limit=10, start=40)
    assert mock_list.call_args.kwargs["limit"] == 10
    assert mock_list.call_args.kwargs["start"] == 40


def test_get_activity_detail(monkeypatch):
    """Activity.get(activity_id) with the client passed through."""
    import mcp_garmin.activity as activity_mod

    fixture = MagicMock()
    fixture_dict = {"activity_id": 123, "distance": 15000}
    mock_client = MagicMock()
    _patch_client(monkeypatch, mock_client)
    with (
        patch("garth.data.Activity.get", return_value=fixture) as mock_get,
        patch("mcp_garmin.client.asdict", return_value=fixture_dict),
    ):
        result = activity_mod.get_activity_detail(activity_id=123)
    mock_get.assert_called_once()
    assert mock_get.call_args.kwargs["activity_id"] == 123
    assert mock_get.call_args.kwargs["client"] is mock_client
    assert result == fixture_dict


def test_get_activity_map(monkeypatch):
    """connectapi path (no /proxy prefix) + both payload keys, snake_cased."""
    import mcp_garmin.activity as activity_mod

    fixture = {
        "activityHeatMapDTO": {"heatmapType": "INTENSITY", "intensityRange": 300},
        "gPolyline": "a]F~FzF~FzF",
    }
    mock_client = MagicMock()
    mock_client.connectapi.return_value = fixture
    _patch_client(monkeypatch, mock_client)

    result = activity_mod.get_activity_map(activity_id=123)

    mock_client.connectapi.assert_called_once_with(
        "/activity-service/activity/123/mapdetails"
    )
    # Both fields present (S2 §5 item 3: heat map + polyline to the client).
    assert result == {
        "activity_heat_map_dto": {
            "heatmap_type": "INTENSITY",
            "intensity_range": 300,
        },
        "g_polyline": "a]F~FzF~FzF",
    }


def test_get_activity_map_none(monkeypatch):
    """connectapi returns None (204) → {} (dict contract preserved)."""
    import mcp_garmin.activity as activity_mod

    mock_client = MagicMock()
    mock_client.connectapi.return_value = None
    _patch_client(monkeypatch, mock_client)

    result = activity_mod.get_activity_map(activity_id=123)

    mock_client.connectapi.assert_called_once_with(
        "/activity-service/activity/123/mapdetails"
    )
    assert result == {}


def test_get_fitness_activities(monkeypatch):
    """FitnessActivity.list(end, days) — client passed through."""
    import mcp_garmin.activity as activity_mod

    fixture = MagicMock()
    fixture_dict = {"calendar_date": "2026-08-31", "total_steps": 20882}
    mock_client = MagicMock()
    _patch_client(monkeypatch, mock_client)
    with (
        patch("garth.data.FitnessActivity.list", return_value=[fixture]) as mock_list,
        patch("mcp_garmin.client.asdict", return_value=fixture_dict),
    ):
        result = activity_mod.get_fitness_activities(end="2026-08-31", days=7)
    mock_list.assert_called_once()
    assert mock_list.call_args.kwargs["end"] == "2026-08-31"
    assert mock_list.call_args.kwargs["days"] == 7
    assert mock_list.call_args.kwargs["client"] is mock_client
    assert result == [fixture_dict]


def test_get_personal_records(monkeypatch):
    """connectapi PR list → per-entry camel_to_snake_dict."""
    import mcp_garmin.activity as activity_mod

    fixture = [
        {"typeId": 12, "value": 5.5},
        {"typeId": 13, "value": 10.2},
    ]
    mock_client = MagicMock()
    mock_client.connectapi.return_value = fixture
    _patch_client(monkeypatch, mock_client)

    result = activity_mod.get_personal_records()

    mock_client.connectapi.assert_called_once_with(
        "/personalrecord-service/personalrecord"
    )
    assert result == [
        {"type_id": 12, "value": 5.5},
        {"type_id": 13, "value": 10.2},
    ]


def test_get_personal_records_none(monkeypatch):
    """connectapi returns None → [] (list contract preserved)."""
    import mcp_garmin.activity as activity_mod

    mock_client = MagicMock()
    mock_client.connectapi.return_value = None
    _patch_client(monkeypatch, mock_client)

    result = activity_mod.get_personal_records()

    assert result == []


def test_get_personal_record_types(monkeypatch):
    """connectapi PR-type list → per-entry camel_to_snake_dict."""
    import mcp_garmin.activity as activity_mod

    fixture = [
        {"typeId": 12, "typeName": "FASTEST_TIME", "unit": "SECONDS"},
    ]
    mock_client = MagicMock()
    mock_client.connectapi.return_value = fixture
    _patch_client(monkeypatch, mock_client)

    result = activity_mod.get_personal_record_types()

    mock_client.connectapi.assert_called_once_with(
        "/personalrecord-service/personalrecordtype"
    )
    assert result == [
        {"type_id": 12, "type_name": "FASTEST_TIME", "unit": "SECONDS"},
    ]


def test_get_personal_record_types_none(monkeypatch):
    """connectapi returns None → [] (list contract preserved)."""
    import mcp_garmin.activity as activity_mod

    mock_client = MagicMock()
    mock_client.connectapi.return_value = None
    _patch_client(monkeypatch, mock_client)

    result = activity_mod.get_personal_record_types()

    assert result == []


# --- tools module: mcp_garmin.tools.activity (same contract, no divergence) ---


def _patch_tools_client(monkeypatch, mock_client):
    import mcp_garmin.tools.activity as tools_activity

    monkeypatch.setattr(tools_activity, "get_client", lambda: mock_client)


def test_tools_get_activities(monkeypatch):
    import mcp_garmin.tools.activity as tools_activity

    fixture = MagicMock()
    fixture_dict = {"activity_id": 456, "type_id": 9}
    mock_client = MagicMock()
    _patch_tools_client(monkeypatch, mock_client)
    with (
        patch("garth.data.Activity.list", return_value=[fixture]) as mock_list,
        patch("mcp_garmin.client.asdict", return_value=fixture_dict),
    ):
        result = tools_activity.get_activities(limit=5, start=10)
    assert mock_list.call_args.kwargs["limit"] == 5
    assert mock_list.call_args.kwargs["start"] == 10
    assert mock_list.call_args.kwargs["client"] is mock_client
    assert result == [fixture_dict]


def test_tools_get_activity_detail(monkeypatch):
    import mcp_garmin.tools.activity as tools_activity

    fixture = MagicMock()
    fixture_dict = {"activity_id": 456, "distance": 12000}
    mock_client = MagicMock()
    _patch_tools_client(monkeypatch, mock_client)
    with (
        patch("garth.data.Activity.get", return_value=fixture) as mock_get,
        patch("mcp_garmin.client.asdict", return_value=fixture_dict),
    ):
        result = tools_activity.get_activity_detail(activity_id=456)
    assert mock_get.call_args.kwargs["activity_id"] == 456
    assert mock_get.call_args.kwargs["client"] is mock_client
    assert result == fixture_dict


def test_tools_get_activity_map(monkeypatch):
    import mcp_garmin.tools.activity as tools_activity

    mock_client = MagicMock()
    mock_client.connectapi.return_value = {
        "activityHeatMapDTO": {"heatmapType": "ELEVATION"},
        "gPolyline": "polyline-string",
    }
    _patch_tools_client(monkeypatch, mock_client)

    result = tools_activity.get_activity_map(activity_id=789)

    mock_client.connectapi.assert_called_once_with(
        "/activity-service/activity/789/mapdetails"
    )
    assert result == {
        "activity_heat_map_dto": {"heatmap_type": "ELEVATION"},
        "g_polyline": "polyline-string",
    }


def test_tools_get_fitness_activities(monkeypatch):
    import mcp_garmin.tools.activity as tools_activity

    fixture = MagicMock()
    fixture_dict = {"calendar_date": "2026-08-31", "total_steps": 19000}
    mock_client = MagicMock()
    _patch_tools_client(monkeypatch, mock_client)
    with (
        patch("garth.data.FitnessActivity.list", return_value=[fixture]) as mock_list,
        patch("mcp_garmin.client.asdict", return_value=fixture_dict),
    ):
        result = tools_activity.get_fitness_activities(end="2026-08-31", days=3)
    assert mock_list.call_args.kwargs["end"] == "2026-08-31"
    assert mock_list.call_args.kwargs["days"] == 3
    assert mock_list.call_args.kwargs["client"] is mock_client
    assert result == [fixture_dict]


def test_tools_get_personal_records(monkeypatch):
    import mcp_garmin.tools.activity as tools_activity

    mock_client = MagicMock()
    mock_client.connectapi.return_value = [{"typeId": 12, "value": 5.5}]
    _patch_tools_client(monkeypatch, mock_client)

    result = tools_activity.get_personal_records()

    mock_client.connectapi.assert_called_once_with(
        "/personalrecord-service/personalrecord"
    )
    assert result == [{"type_id": 12, "value": 5.5}]


def test_tools_get_personal_record_types(monkeypatch):
    import mcp_garmin.tools.activity as tools_activity

    mock_client = MagicMock()
    mock_client.connectapi.return_value = [{"typeId": 12, "typeName": "FASTEST_TIME"}]
    _patch_tools_client(monkeypatch, mock_client)

    result = tools_activity.get_personal_record_types()

    mock_client.connectapi.assert_called_once_with(
        "/personalrecord-service/personalrecordtype"
    )
    assert result == [{"type_id": 12, "type_name": "FASTEST_TIME"}]
