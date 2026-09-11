"""Contract test for the tool surface — the garth-ng migration norm-anchor.

This file is the GATING norm-anchor (WP-01) for the garth -> garth-ng 1.1.0
migration. It pins the *target* tool surface that every downstream work
package (WP-02..WP-16) must converge on:

    * exactly 38 tools (40 legacy - 2 documented Device-Drops),
    * ``get_activities(limit: int = 20, start: int = 0)`` (was
      ``(end, days)`` — documented breaking change, S2 open-item 7),
    * all tool names snake_case, payloads snake_case / ISO-8601, weight in
      grams (the payload-shape contract, unchanged vs. main).

Target surface
--------------
``TARGET_TOOLS`` below is the authoritative spec: name -> (params, return).
Each param is a ``(name, default)`` tuple; a default of ``inspect.Parameter.empty``
means the parameter is required. This spec is self-contained (a frozen
constant), so the anchor is defined independently of whatever the *current*
registry holds — it is the norm, not a snapshot of today's code.

Relationship to the live registry
---------------------------------
``test_live_registry_converges_to_target`` compares the pinned target against
the tools actually registered in ``mcp_garmin.tools``. While the migration WPs
are landing it reports the remaining drift (the 2 Device-Drops and the
``get_activities`` signature flip). It is an ``xfail`` gate: it is *expected*
to fail until WP-11 (``get_activities`` signature) + WP-14 (device drops) have
landed, and the migration WPs are expected to flip it green — not to relax it.
With ``strict=False`` the file stays green in both states (xfailed now, xpassed
once the WPs land).

Shape checks
------------
``test_return_shapes_against_mocks`` verifies, against mocks (no network), that
each target tool returns the pinned shape (``dict`` or ``list[dict]``). The
mocks intercept the garth accessor the *current* code calls (``garth.data.<Name>``
+ the module's ``get_client``), so no live client or network is touched.
"""

from __future__ import annotations

import importlib
import inspect
import sys
from unittest.mock import MagicMock, patch

import pytest

# Ensure the package source is importable regardless of how pytest is invoked.
_SRC = str(__import__("pathlib").Path(__file__).resolve().parents[2] / "src")
if _SRC not in sys.path:
    sys.path.insert(0, _SRC)

from mcp_garmin.tools import base  # noqa: E402

# ---------------------------------------------------------------------------
# Target surface (the norm) — 38 tools.
# ---------------------------------------------------------------------------

_EMPTY = inspect.Parameter.empty

# name -> (params, return_annotation)
# params is a list of (name, default); default=_EMPTY means "required".
TARGET_TOOLS: dict[str, tuple[list[tuple[str, object]], str]] = {
    # --- activity (6) ---
    # Signature change (breaking, S2 open-item 7): (end, days) -> (limit, start).
    "get_activities": ([("limit", 20), ("start", 0)], "list[dict]"),
    "get_activity_detail": ([("activity_id", _EMPTY)], "dict"),
    "get_activity_map": ([("activity_id", _EMPTY)], "dict"),
    "get_fitness_activities": ([("end", None), ("days", 7)], "list[dict]"),
    "get_personal_records": ([], "list[dict]"),
    "get_personal_record_types": ([], "list[dict]"),
    # --- body (6) ---
    "get_body_weight": ([("day", None)], "dict"),
    "get_weight_history": ([("end", None), ("days", 7)], "list[dict]"),
    "get_blood_pressure": ([("day", None)], "dict"),
    "get_body_battery": ([("day", None)], "list[dict]"),
    "get_body_battery_stress": ([("day", None)], "dict"),
    "get_body_battery_stress_history": ([("end", None), ("days", 7)], "list[dict]"),
    # --- heart (3) ---
    "get_daily_heart_rate": ([("day", None)], "list[dict]"),
    "get_hrv": ([("day", None)], "list[dict]"),
    "get_resting_heart_rate": ([("day", None)], "dict"),
    # --- sleep (3) ---
    "get_sleep": ([("day", None)], "list[dict]"),
    "get_sleep_detail": ([("day", None)], "dict"),
    "get_sleep_summary": ([("day", None)], "dict"),
    # --- stress / training / readiness (7) ---
    "get_daily_stress": ([("day", None)], "list[dict]"),
    "get_weekly_stress": ([("start_date", None)], "list[dict]"),
    "get_training_status_daily": ([("day", None)], "dict"),
    "get_training_status_weekly": ([("start_date", None)], "dict"),
    "get_training_status_monthly": ([("start_date", None)], "dict"),
    "get_training_readiness": ([("day", None)], "dict"),
    "get_morning_readiness": ([("day", None)], "dict"),
    # --- steps / summary (4) ---
    "get_daily_steps": ([("day", None)], "dict"),
    "get_weekly_steps": ([("start_date", None)], "list[dict]"),
    "get_daily_summary": ([("day", None)], "dict"),
    "get_daily_summary_history": ([("end", None), ("days", 7)], "list[dict]"),
    # --- hydration (2) ---
    "get_daily_hydration": ([("day", None)], "dict"),
    "get_hydration_history": ([("end", None), ("days", 7)], "list[dict]"),
    # --- nutrition (2) ---
    "get_nutrition_log": ([("day", None)], "list[dict]"),
    "get_nutrition_status": ([("day", None)], "dict"),
    # --- goals (3) ---
    "get_steps_goal": ([], "dict"),
    "get_weight_goal": ([], "dict"),
    "get_garmin_scores": ([], "dict"),
    # --- util (2) ---
    "get_user_profile": ([], "dict"),
    "get_user_settings": ([], "dict"),
}

# Tools removed by the migration (documented Device-Drops — S2 §3, S1 Run
# #49/#51: no garth-ng device domain, all connectapi variants 404). Must NOT
# appear in the target surface.
DROPPED_DEVICE_TOOLS = {"get_connected_devices", "get_device_info"}


def _live_registry() -> dict[str, object]:
    """Return the registered tool functions keyed by name (side-effect: imports).

    Modules are imported defensively: a tool module that a migration work
    package has already removed (e.g. ``devices`` after WP-14) is skipped
    instead of raising, so this anchor stays valid — and can flip green — at
    the moment the migration completes rather than erroring on the import.
    """
    for _mod in (
        "body",
        "heart",
        "sleep",
        "stress",
        "steps",
        "hydration",
        "activity",
        "devices",
        "nutrition",
        "goals",
        "util",
    ):
        try:
            importlib.import_module(f"mcp_garmin.tools.{_mod}")
        except ImportError:
            continue
    return {f.__name__: f for f in base.get_registered_tools()}


def _param_view(func: object) -> list[tuple[str, object]]:
    """(name, default) pairs for a callable, matching the TARGET_TOOLS format."""
    sig = inspect.signature(func)
    view: list[tuple[str, object]] = []
    for p in sig.parameters.values():
        view.append((p.name, _EMPTY if p.default is _EMPTY else p.default))
    return view


def _return_view(func: object) -> str:
    return str(inspect.signature(func).return_annotation)


# ---------------------------------------------------------------------------
# 1. The pinned anchor is self-consistent.
# ---------------------------------------------------------------------------


def test_target_surface_pins_38_tools() -> None:
    """The target surface is exactly the 38 migrated tools."""
    assert len(TARGET_TOOLS) == 38, (
        f"Target surface must pin exactly 38 tools, found {len(TARGET_TOOLS)}: "
        f"{sorted(TARGET_TOOLS)}"
    )
    assert len(set(TARGET_TOOLS)) == 38, "Target surface contains duplicate tool names."


def test_target_surface_has_no_device_tools() -> None:
    """The 2 Device-Drops are absent from the pinned surface."""
    dropped = set(TARGET_TOOLS) & DROPPED_DEVICE_TOOLS
    assert (
        not dropped
    ), f"Device tools must be dropped from the target surface: {sorted(dropped)}"


def test_target_surface_get_activities_uses_limit_start() -> None:
    """get_activities is pinned to (limit: int = 20, start: int = 0)."""
    params, ret = TARGET_TOOLS["get_activities"]
    assert params == [
        ("limit", 20),
        ("start", 0),
    ], f"get_activities must be (limit=20, start=0), got {params}"
    assert ret == "list[dict]", f"get_activities must return list[dict], got {ret!r}"


def test_target_surface_names_are_snake_case() -> None:
    """Every pinned tool name is snake_case (lowercase, underscore-separated)."""
    bad = [
        n
        for n in TARGET_TOOLS
        if not n.isidentifier()
        or not all(c.islower() or c == "_" or c.isdigit() for c in n)
    ]
    assert not bad, f"Non-snake_case tool names in target surface: {sorted(bad)}"


# ---------------------------------------------------------------------------
# 2. The live registry converges to the target (gating drift report).
# ---------------------------------------------------------------------------


@pytest.mark.xfail(
    strict=False,
    reason=(
        "Live registry converges to the pinned 38-tool target once WP-11 "
        "(get_activities -> limit/start) and WP-14 (device drops) have landed. "
        "Expected-fail (xfailed) until then; the migration WPs flip this gate "
        "green rather than relaxing it. strict=False keeps the file green in "
        "both states (xfailed now, xpassed once converged)."
    ),
)
def test_live_registry_converges_to_target() -> None:
    """Compare the registered tools against the pinned 38-tool target surface."""
    live = _live_registry()
    target_names = set(TARGET_TOOLS)
    live_names = set(live)

    problems: list[str] = []

    # (a) A pinned target tool missing from the live registry.
    missing = target_names - live_names
    if missing:
        problems.append(f"pinned tools missing from live registry: {sorted(missing)}")

    # (b) A live tool not in the pinned target (expected: the 2 device drops).
    extra = live_names - target_names
    if extra:
        problems.append(f"live tools not in pinned target surface: {sorted(extra)}")

    # (c) Signature drift on tools present on both sides.
    sig_drift: list[str] = []
    for name in sorted(target_names & live_names):
        params, ret = TARGET_TOOLS[name]
        live_params = _param_view(live[name])
        live_ret = _return_view(live[name])
        if live_params != params:
            sig_drift.append(f"{name}: params {live_params} != pinned {params}")
        elif live_ret != ret:
            sig_drift.append(f"{name}: return {live_ret!r} != pinned {ret!r}")
    if sig_drift:
        problems.append("signature/return drift: " + "; ".join(sig_drift))

    assert not problems, (
        "Live registry has not converged to the pinned 38-tool target surface:\n  - "
        + "\n  - ".join(problems)
    )


# ---------------------------------------------------------------------------
# 3. Return shapes, verified against mocks (no network).
# ---------------------------------------------------------------------------

# name -> (module, garth.data accessor name, accessor method, call-kwargs, shape)
# The accessor name/method must match what the *current* code calls for the mock
# to intercept it; update the name (one line) when a migration WP renames an
# accessor. ``call_kwargs`` supplies required positional args (e.g. activity_id).
# The shape contract (dict / list[dict]) does not change across the migration.
_SHAPE_TOOLS: dict[str, tuple[str, str, str, dict[str, object], str]] = {
    # --- activity ---
    "get_activities": ("activity", "Activities", "list", {}, "list[dict]"),
    "get_activity_detail": (
        "activity",
        "ActivityDetail",
        "get",
        {"activity_id": "1"},
        "dict",
    ),
    "get_activity_map": (
        "activity",
        "ActivityMap",
        "get",
        {"activity_id": "1"},
        "dict",
    ),
    "get_fitness_activities": (
        "activity",
        "FitnessActivities",
        "list",
        {},
        "list[dict]",
    ),
    "get_personal_records": ("activity", "PersonalRecords", "get", {}, "list[dict]"),
    "get_personal_record_types": (
        "activity",
        "PersonalRecordTypes",
        "get",
        {},
        "list[dict]",
    ),
    # --- body ---
    "get_body_weight": ("body", "WeightData", "get", {}, "dict"),
    "get_weight_history": ("body", "WeightData", "list", {}, "list[dict]"),
    "get_blood_pressure": ("body", "BloodPressure", "get", {}, "dict"),
    "get_body_battery": ("body", "BodyBatteryData", "get", {}, "list[dict]"),
    "get_body_battery_stress": ("body", "DailyBodyBatteryStress", "get", {}, "dict"),
    "get_body_battery_stress_history": (
        "body",
        "DailyBodyBatteryStress",
        "list",
        {},
        "list[dict]",
    ),
    # --- heart ---
    "get_daily_heart_rate": ("heart", "HeartRateData", "get", {}, "list[dict]"),
    "get_hrv": ("heart", "HrvData", "get", {}, "list[dict]"),
    "get_resting_heart_rate": ("heart", "RestingHeartRateData", "get", {}, "dict"),
    # --- sleep ---
    "get_sleep": ("sleep", "SleepData", "get", {}, "list[dict]"),
    "get_sleep_detail": ("sleep", "DailySleepData", "get", {}, "dict"),
    "get_sleep_summary": ("sleep", "DailySleepData", "get", {}, "dict"),
    # --- stress / training / readiness ---
    "get_daily_stress": ("stress", "DailyStressData", "get", {}, "list[dict]"),
    "get_weekly_stress": ("stress", "WeeklyStressData", "get", {}, "list[dict]"),
    "get_training_status_daily": ("stress", "TrainingStatusDaily", "get", {}, "dict"),
    "get_training_status_weekly": ("stress", "TrainingStatusWeekly", "get", {}, "dict"),
    "get_training_status_monthly": (
        "stress",
        "TrainingStatusMonthly",
        "get",
        {},
        "dict",
    ),
    "get_training_readiness": ("stress", "TrainingReadiness", "get", {}, "dict"),
    "get_morning_readiness": ("stress", "MorningReadiness", "get", {}, "dict"),
    # --- steps / summary ---
    "get_daily_steps": ("steps", "StepsData", "get", {}, "dict"),
    "get_weekly_steps": ("steps", "WeeklyStepsData", "get", {}, "list[dict]"),
    "get_daily_summary": ("steps", "DailySummary", "get", {}, "dict"),
    "get_daily_summary_history": ("steps", "DailySummary", "list", {}, "list[dict]"),
    # --- hydration ---
    "get_daily_hydration": ("hydration", "HydrationData", "get", {}, "dict"),
    "get_hydration_history": ("hydration", "HydrationData", "list", {}, "list[dict]"),
    # --- nutrition ---
    "get_nutrition_log": ("nutrition", "NutritionLog", "get", {}, "list[dict]"),
    "get_nutrition_status": ("nutrition", "NutritionStatus", "get", {}, "dict"),
    # --- goals ---
    "get_steps_goal": ("goals", "StepsGoal", "get", {}, "dict"),
    "get_weight_goal": ("goals", "WeightGoal", "get", {}, "dict"),
    "get_garmin_scores": ("goals", "GarminScores", "get", {}, "dict"),
    # --- util ---
    "get_user_profile": ("util", "UserProfile", "get", {}, "dict"),
    "get_user_settings": ("util", "UserSettings", "get", {}, "dict"),
}


def _sleep_mock() -> MagicMock:
    """Mock for get_sleep: the code reads .daily_sleep_dto (dict) + .sleep_movement (list)."""
    return MagicMock(
        daily_sleep_dto={"calendar_date": "2026-09-01"},
        sleep_movement=[{"type": "LIGHT"}],
    )


def _check_shape(name: str, monkeypatch) -> None:
    module, accessor, method, call_kwargs, expected = _SHAPE_TOOLS[name]
    mod = importlib.import_module(f"mcp_garmin.tools.{module}")
    # No network: the module's get_client returns a mock (the client is only
    # passed through to the mocked accessor).
    monkeypatch.setattr(mod, "get_client", lambda: MagicMock())

    if name == "get_sleep":
        ret: object = _sleep_mock()
    elif expected == "dict":
        ret = {"k": "v"}
    else:
        ret = [{"k": "v"}]

    with patch(f"garth.data.{accessor}", create=True) as acc:
        getattr(acc, method).return_value = ret
        result = getattr(mod, name)(**call_kwargs)

    if expected == "list[dict]":
        assert isinstance(
            result, list
        ), f"{name}: expected list[dict], got {type(result).__name__}"
        assert all(
            isinstance(item, dict) for item in result
        ), f"{name}: list contains non-dict items"
    else:
        assert isinstance(
            result, dict
        ), f"{name}: expected dict, got {type(result).__name__}"


@pytest.mark.parametrize("name", sorted(TARGET_TOOLS))
def test_return_shapes_against_mocks(name: str, monkeypatch) -> None:
    """Each pinned tool returns the pinned shape (dict / list[dict]) against mocks."""
    assert name in _SHAPE_TOOLS, f"Missing shape spec for pinned tool {name!r}."
    _check_shape(name, monkeypatch)
