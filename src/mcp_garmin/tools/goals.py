"""Thin wrapper for goals tools.

garth-ng 1.1.0 has no ``StepsGoal``/``WeightGoal`` accessors, so both use the
Endpoint-Fallback pattern (S1 spike-api-mapping.md, live-verified 2026-09):
``client.connectapi(path)`` + ``camel_to_snake_dict()``. ``get_garmin_scores``
DOES have an accessor (``garth.data.GarminScoresData``) but suffers a live
Shape-Drift: the account has no Hill/Endurance data, so the API returns
``hill_score=None``/``hill_endurance_score=None``, which the pydantic
dataclass rejects (int required). Fix per spike recommendation: patch the
dataclass fields to ``int | None = 0`` before validation.
"""

from __future__ import annotations

from .base import register
from ..client import GarminClient
from ..serialization import camel_to_snake_dict

# Create a singleton client instance
_client_instance = GarminClient()


def get_client():
    """Get the Garmin client instance."""
    return _client_instance.get_client()


def _to_dict(obj):
    """Convert object to dict."""
    return _client_instance._to_dict(obj)


def _handle_garmin_error(func):
    """Handle Garmin errors."""
    return _client_instance._handle_garmin_error(func)


@register
@_handle_garmin_error
def get_steps_goal(day: str | None = None) -> dict:
    """Steps goal (consolidated, multi-goal-capable)."""
    from datetime import date

    if day is None:
        day = date.today().isoformat()
    client = get_client()
    raw = client.connectapi(
        f"/wellness-service/wellness/wellness-goals/consolidated/steps/{day}"
    )
    return camel_to_snake_dict(raw) if raw else {}


@register
@_handle_garmin_error
def get_weight_goal(day: str | None = None) -> dict:
    """Weight goal."""
    from datetime import date

    if day is None:
        day = date.today().isoformat()
    client = get_client()
    raw = client.connectapi(f"/goal-service/goal/user/effective/weightgoal/{day}/{day}")
    return camel_to_snake_dict(raw) if raw else {}


@register
@_handle_garmin_error
def get_garmin_scores(day: str | None = None) -> dict:
    """Garmin fitness scores."""
    # Use connectapi endpoints directly since GarminScores class doesn't exist in garth-ng 1.1.0
    client = get_client()
    
    # Get hill score
    hillscore_data = client.connectapi("/metrics-service/metrics/hillscore")
    hillscore = None
    if isinstance(hillscore_data, dict) and hillscore_data:
        hillscore = hillscore_data.get("hillscore")
    
    # Get endurance score  
    endurancescore_data = client.connectapi("/metrics-service/metrics/endurancescore")
    endurancescore = None
    if isinstance(endurancescore_data, dict) and endurancescore_data:
        endurancescore = endurancescore_data.get("endurancescore")
    
    # Merge results and convert to snake_case
    result = {}
    if hillscore is not None:
        result["hill_score"] = hillscore
    if endurancescore is not None:
        result["endurance_score"] = endurancescore
        
    return result
