"""Contract test for the tool surface (WP-01 anchor, S2 spike-scope.md: 38 tools)."""

import importlib

from mcp_garmin.tools import base


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


def test_tool_surface_contract():
    """Registered tool set matches the frozen 38-tool target surface (WP-01)."""
    registered_tools = sorted(_live_registry().keys())

    expected_tools = sorted(
        [
            # body
            "get_body_weight",
            "get_weight_history",
            "get_blood_pressure",
            "get_body_battery",
            "get_body_battery_stress",
            "get_body_battery_stress_history",
            # heart
            "get_daily_heart_rate",
            "get_hrv",
            "get_resting_heart_rate",
            # sleep
            "get_sleep",
            "get_sleep_detail",
            "get_sleep_summary",
            # stress
            "get_daily_stress",
            "get_weekly_stress",
            "get_training_status_daily",
            "get_training_status_weekly",
            "get_training_status_monthly",
            "get_training_readiness",
            "get_morning_readiness",
            # steps
            "get_daily_steps",
            "get_weekly_steps",
            "get_daily_summary",
            "get_daily_summary_history",
            # hydration
            "get_daily_hydration",
            "get_hydration_history",
            # activity
            "get_activities",
            "get_activity_detail",
            "get_activity_map",
            "get_fitness_activities",
            "get_personal_records",
            "get_personal_record_types",
            # nutrition
            "get_nutrition_log",
            "get_nutrition_status",
            # goals
            "get_steps_goal",
            "get_weight_goal",
            "get_garmin_scores",
            # util
            "get_user_profile",
            "get_user_settings",
        ]
    )

    assert registered_tools == expected_tools, (
        f"Tool surface drift.\n"
        f"  missing: {sorted(set(expected_tools) - set(registered_tools))}\n"
        f"  unexpected: {sorted(set(registered_tools) - set(expected_tools))}"
    )
    assert len(expected_tools) == 38
