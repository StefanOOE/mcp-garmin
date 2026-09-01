"""MCP server exposing Garmin Connect fitness data as tools."""
from __future__ import annotations

from mcp.server import MCPServer

from .activity import (
    get_activities,
    get_activity_detail,
    get_activity_map,
    get_fitness_activities,
    get_personal_record_types,
    get_personal_records,
)
from .body import (
    get_blood_pressure,
    get_body_battery,
    get_body_battery_stress,
    get_body_battery_stress_history,
    get_body_weight,
    get_weight_history,
)
from .devices import get_connected_devices, get_device_info
from .goals import get_garmin_scores, get_steps_goal, get_weight_goal
from .heart import get_daily_heart_rate, get_hrv, get_resting_heart_rate
from .hydration import get_daily_hydration, get_hydration_history
from .nutrition import get_nutrition_log, get_nutrition_status
from .sleep import get_sleep, get_sleep_detail, get_sleep_summary
from .steps import (
    get_daily_steps,
    get_daily_summary,
    get_daily_summary_history,
    get_weekly_steps,
)
from .stress import (
    get_daily_stress,
    get_morning_readiness,
    get_training_readiness,
    get_training_status_daily,
    get_training_status_monthly,
    get_training_status_weekly,
    get_weekly_stress,
)
from .util import get_user_profile, get_user_settings

mcp = MCPServer(
    "mcp-garmin",
    version="0.1.0",
    instructions=(
        "Garmin Connect fitness data as fine-grained MCP tools. "
        "Returns snake_case JSON dicts. Use get_user_profile() for identity, "
        "get_body_weight() for weight, get_sleep_summary() for sleep, "
        "get_daily_heart_rate() for HR, get_daily_stress() for stress. "
        "All timestamps are ISO 8601 or YYYY-MM-DD date strings. "
        "Weight is in grams (e.g. 95010 = 95.01 kg). Steps are integers. "
        "Calories are in kcal. If a tool returns a German ToolError message, "
        "the Garmin token is likely expired — re-run garmin_login.py."
    ),
)

_ALL_TOOLS = (
    # body
    get_body_weight,
    get_weight_history,
    get_blood_pressure,
    get_body_battery,
    get_body_battery_stress,
    get_body_battery_stress_history,
    # heart
    get_daily_heart_rate,
    get_hrv,
    get_resting_heart_rate,
    # sleep
    get_sleep,
    get_sleep_detail,
    get_sleep_summary,
    # stress
    get_daily_stress,
    get_weekly_stress,
    get_training_status_daily,
    get_training_status_weekly,
    get_training_status_monthly,
    get_training_readiness,
    get_morning_readiness,
    # steps
    get_daily_steps,
    get_weekly_steps,
    get_daily_summary,
    get_daily_summary_history,
    # hydration
    get_daily_hydration,
    get_hydration_history,
    # activity
    get_activities,
    get_activity_detail,
    get_activity_map,
    get_fitness_activities,
    get_personal_records,
    get_personal_record_types,
    # devices
    get_device_info,
    get_connected_devices,
    # nutrition
    get_nutrition_log,
    get_nutrition_status,
    # goals
    get_steps_goal,
    get_weight_goal,
    get_garmin_scores,
    # util
    get_user_profile,
    get_user_settings,
)

for _fn in _ALL_TOOLS:
    mcp.tool()(_fn)


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
