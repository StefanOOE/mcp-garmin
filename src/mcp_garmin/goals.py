"""Goal-Tools: Schritte-Ziel, Gewicht-Ziel, Garmin Fitness-Scores."""
from __future__ import annotations

from .client import _handle_garmin_error, _to_dict, get_client


@_handle_garmin_error
def get_steps_goal(day: str | None = None) -> dict:
    """Schritte-Ziel für einen Tag (YYYY-MM-DD) — Gerät + Nutzer + Sync-Status."""
    client = get_client()
    from garth.data import StepsGoal

    result = StepsGoal.get(day=day, client=client)
    return _to_dict(result) if result is not None else {}


@_handle_garmin_error
def get_weight_goal(day: str | None = None) -> dict:
    """Gewichts-Ziel für einen Tag (YYYY-MM-DD) — Ziel + Zielbereiche."""
    client = get_client()
    from garth.data import WeightGoal

    result = WeightGoal.get(day=day, client=client)
    return _to_dict(result) if result is not None else {}


@_handle_garmin_error
def get_garmin_scores(day: str | None = None) -> dict:
    """Garmin Fitness-Scores für einen Tag (YYYY-MM-DD) — Vo2Max, Endurance, Power."""
    client = get_client()
    import garth

    result = garth.GarminScoresData.get(day=day, client=client)
    return _to_dict(result) if result is not None else {}
