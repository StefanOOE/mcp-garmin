# mcp-garmin

MCP server exposing Garmin Connect fitness data as 39 fine-grained tools.

## Setup

```bash
cd /home/ss/src/mcp-garmin
python -m venv .venv
.venv/bin/pip install -e ".[dev]"
```

## Authentication (one-time)

```bash
.venv/bin/python garmin_login.py
```

Tokens are stored in `~/.garth/oauth2_token.json` and expire after ~24h.
Re-run `garmin_login.py` when the token expires.

## Running

```bash
.venv/bin/python -m mcp_garmin
```

## Tools (39)

| Category | Tools |
|----------|-------|
| **Body** (6) | `get_body_weight`, `get_weight_history`, `get_blood_pressure`, `get_body_battery`, `get_body_battery_stress`, `get_body_battery_stress_history` |
| **Heart** (3) | `get_daily_heart_rate`, `get_hrv`, `get_resting_heart_rate` |
| **Sleep** (3) | `get_sleep`, `get_sleep_detail`, `get_sleep_summary` |
| **Stress** (7) | `get_daily_stress`, `get_weekly_stress`, `get_training_status_daily`, `get_training_status_weekly`, `get_training_status_monthly`, `get_training_readiness`, `get_morning_readiness` |
| **Activity** (6) | `get_activities`, `get_activity_detail`, `get_activity_map`, `get_fitness_activities`, `get_personal_records`, `get_personal_record_types` |
| **Steps** (4) | `get_daily_steps`, `get_weekly_steps`, `get_daily_summary`, `get_daily_summary_history` |
| **Hydration** (2) | `get_daily_hydration`, `get_hydration_history` |
| **Devices** (2) | `get_device_info`, `get_connected_devices` |
| **Nutrition** (2) | `get_nutrition_log`, `get_nutrition_status` |
| **Goals** (3) | `get_steps_goal`, `get_weight_goal`, `get_garmin_scores` |
| **Util** (2) | `get_user_profile`, `get_user_settings` |

## Data Format

- All timestamps are ISO 8601 or `YYYY-MM-DD` date strings
- Weight is in **grams** (e.g. `95010` = 95.01 kg)
- Steps are integers
- Calories are in kcal
- All keys are `snake_case`
- If a tool returns a German `ToolError` message, the Garmin token is likely expired — re-run `garmin_login.py`

## Tests

```bash
.venv/bin/python -m pytest tests/ -v
.venv/bin/python -m ruff check src/ tests/
```