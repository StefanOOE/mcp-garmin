"""Thin wrapper for goals tools."""

from __future__ import annotations

from .base import register
from ..client import GarminClient


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
def get_steps_goal() -> dict:
    """Steps goal."""
    from garth.data import StepsGoal
    client = get_client()
    result = StepsGoal.get(client=client)
    return _to_dict(result)


@register
@_handle_garmin_error
def get_weight_goal() -> dict:
    """Weight goal."""
    from garth.data import WeightGoal
    client = get_client()
    result = WeightGoal.get(client=client)
    return _to_dict(result)


@register
@_handle_garmin_error
def get_garmin_scores() -> dict:
    """Garmin fitness scores."""
    from garth.data import GarminScores
    client = get_client()
    result = GarminScores.get(client=client)
    return _to_dict(result)