"""Body-Tools: Gewicht, Blutdruck, Body Battery."""
from __future__ import annotations

from .client import _handle_garmin_error, _to_dict, get_client


@_handle_garmin_error
def get_body_weight(day: str | None = None) -> dict:
    """Körpergewicht für einen Tag (YYYY-MM-DD) — Gramm, BMI, Körperfett usw."""
    client = get_client()
    from garth.data import WeightData

    result = WeightData.get(day=day, client=client)
    return _to_dict(result)


@_handle_garmin_error
def get_weight_history(end: str | None = None, days: int = 7) -> list[dict]:
    """Gewichtsverlauf der letzten N Tage (bis end, YYYY-MM-DD)."""
    client = get_client()
    from garth.data import WeightData

    result = WeightData.list(end=end, days=days, client=client)
    return [_to_dict(entry) for entry in result]


@_handle_garmin_error
def get_blood_pressure(day: str | None = None) -> dict:
    """Blutdruckmessung für einen Tag (YYYY-MM-DD)."""
    client = get_client()
    from garth.data import BloodPressure

    result = BloodPressure.get(day=day, client=client)
    return _to_dict(result)


@_handle_garmin_error
def get_body_battery(day: str | None = None) -> list[dict]:
    """Body-Battery-Messwerte für einen Tag (YYYY-MM-DD)."""
    client = get_client()
    from garth.data import BodyBatteryData

    result = BodyBatteryData.get(day=day, client=client)
    return [_to_dict(entry) for entry in result]


@_handle_garmin_error
def get_body_battery_stress(day: str | None = None) -> dict:
    """Body-Battery- + Stress-Zusammenfassung für einen Tag (YYYY-MM-DD)."""
    client = get_client()
    from garth.data import DailyBodyBatteryStress

    result = DailyBodyBatteryStress.get(day=day, client=client)
    return _to_dict(result)


@_handle_garmin_error
def get_body_battery_stress_history(end: str | None = None, days: int = 7) -> list[dict]:
    """Body-Battery- + Stress-Verlauf der letzten N Tage (bis end)."""
    client = get_client()
    from garth.data import DailyBodyBatteryStress

    result = DailyBodyBatteryStress.list(end=end, days=days, client=client)
    return [_to_dict(entry) for entry in result]
