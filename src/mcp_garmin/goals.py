"""Goal tools: steps goal, weight goal, Garmin fitness scores."""
from __future__ import annotations

from .client import _handle_garmin_error, _to_dict, get_client


@_handle_garmin_error
def get_steps_goal(day: str | None = None) -> dict:
    """Steps goal for a day (YYYY-MM-DD) — device + user + sync status."""
    client = get_client()
    from garth.data import StepsGoal

    result = StepsGoal.get(day=day, client=client)
    return _to_dict(result) if result is not None else {}


@_handle_garmin_error
def get_weight_goal(day: str | None = None) -> dict:
    """Weight goal for a day (YYYY-MM-DD) — target + target ranges."""
    client = get_client()
    from garth.data import WeightGoal

    result = WeightGoal.get(day=day, client=client)
    return _to_dict(result) if result is not None else {}


@_handle_garmin_error
def get_garmin_scores(day: str | None = None) -> dict:
    """Garmin fitness scores for a day (YYYY-MM-DD) — Vo2Max, Endurance, Power."""
    client = get_client()
    import garth

    result = garth.GarminScoresData.get(day=day, client=client)
    return _to_dict(result) if result is not None else {}
