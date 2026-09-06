"""Contract test for the tool surface."""

from mcp_garmin.tools.base import get_tool_names


def test_tool_surface_contract():
    """Test that the registered tool set matches the expected frozen list."""
    # Get the names of all registered tools
    registered_tools = sorted(get_tool_names())

    # The expected tool names from the original 40 tools
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
            # devices
            "get_connected_devices",
            "get_device_info",
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

    # Check that the registered tools match the expected set
    assert (
        registered_tools == expected_tools
    ), f"Expected {expected_tools}, but got {registered_tools}"
