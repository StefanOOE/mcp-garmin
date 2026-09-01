"""Body tools: weight, blood pressure, body battery."""
from __future__ import annotations

from .client import _handle_garmin_error, _to_dict, get_client


@_handle_garmin_error
def get_body_weight(day: str | None = None) -> dict:
    """Body weight for a day (YYYY-MM-DD) — grams, BMI, body fat, etc."""
    client = get_client()
    from garth.data import WeightData

    result = WeightData.get(day=day, client=client)
    return _to_dict(result)


@_handle_garmin_error
def get_weight_history(end: str | None = None, days: int = 7) -> list[dict]:
    """Weight history for the last N days (up to end, YYYY-MM-DD)."""
    client = get_client()
    from garth.data import WeightData

    result = WeightData.list(end=end, days=days, client=client)
    return [_to_dict(entry) for entry in result]


@_handle_garmin_error
def get_blood_pressure(day: str | None = None) -> dict:
    """Blood pressure reading for a day (YYYY-MM-DD)."""
    client = get_client()
    from garth.data import BloodPressure

    result = BloodPressure.get(day=day, client=client)
    return _to_dict(result)


@_handle_garmin_error
def get_body_battery(day: str | None = None) -> list[dict]:
    """Body Battery readings for a day (YYYY-MM-DD)."""
    client = get_client()
    from garth.data import BodyBatteryData

    result = BodyBatteryData.get(day=day, client=client)
    return [_to_dict(entry) for entry in result]


@_handle_garmin_error
def get_body_battery_stress(day: str | None = None) -> dict:
    """Body Battery + stress summary for a day (YYYY-MM-DD)."""
    client = get_client()
    from garth.data import DailyBodyBatteryStress

    result = DailyBodyBatteryStress.get(day=day, client=client)
    return _to_dict(result)


@_handle_garmin_error
def get_body_battery_stress_history(end: str | None = None, days: int = 7) -> list[dict]:
    """Body Battery + stress history for the last N days (up to end)."""
    client = get_client()
    from garth.data import DailyBodyBatteryStress

    result = DailyBodyBatteryStress.list(end=end, days=days, client=client)
    return [_to_dict(entry) for entry in result]
