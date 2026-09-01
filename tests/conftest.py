"""Shared pytest fixtures for mcp-garmin."""
from __future__ import annotations

from unittest.mock import MagicMock
import pytest


@pytest.fixture
def mock_client() -> MagicMock:
    """Mocked garth http.Client for all tool tests."""
    client = MagicMock()
    client.connectapi = MagicMock()
    return client


@pytest.fixture
def weight_fixture() -> dict:
    """Realistic WeightData dict (verified 2026-09-01)."""
    return {
        "weight": 95010,
        "bmi": 28.4,
        "body_fat": 28.5,
        "body_water": 52.2,
        "bone_mass": 4869,
        "muscle_mass": 35319,
        "visceral_fat": None,
        "metabolic_age": None,
        "physique_rating": None,
        "calendar_date": "2026-09-01",
        "timestamp_gmt": 1788153326000,
        "timestamp_local": 1788153326000,
        "source_type": "INDEX_SCALE",
        "sample_pk": 1788146153109,
        "weight_delta": -500.0,
    }


@pytest.fixture
def daily_steps_fixture() -> dict:
    """Realistic DailySteps dict (verified 2026-09-01)."""
    return {
        "calendar_date": "2026-08-31",
        "total_steps": 20882,
        "total_distance": 17389,
        "step_goal": 10000,
    }


@pytest.fixture
def daily_hrv_fixture() -> dict:
    """Realistic DailyHRV dict (verified 2026-09-01)."""
    return {
        "calendar_date": "2026-08-31",
        "weekly_avg": 37,
        "last_night_avg": 42,
        "last_night_5_min_high": 74,
        "baseline": {"low_upper": 34, "balanced_low": 36, "balanced_upper": 45},
        "status": "BALANCED",
        "feedback_phrase": "HRV_BALANCED_2",
    }


@pytest.fixture
def daily_stress_fixture() -> dict:
    """Realistic DailyStress dict (verified 2026-09-01)."""
    return {
        "calendar_date": "2026-08-31",
        "overall_stress_level": 23,
        "rest_stress_duration": 43320,
        "low_stress_duration": 20820,
        "medium_stress_duration": 1500,
        "high_stress_duration": 120,
    }


@pytest.fixture
def daily_summary_fixture() -> dict:
    """Realistic DailySummary dict (verified 2026-09-01)."""
    return {
        "calendar_date": "2026-08-31",
        "total_steps": 20882,
        "total_kilocalories": 2800,
        "active_kilocalories": 1200,
        "total_distance_meters": 17389,
        "resting_heart_rate": 52,
        "max_heart_rate": 178,
        "min_heart_rate": 48,
        "body_battery_at_wake_time": 78,
        "sleeping_seconds": 25200,
        "active_seconds": 7200,
    }


@pytest.fixture
def user_profile_fixture() -> dict:
    """Realistic UserProfile dict (verified 2026-09-01)."""
    return {
        "display_name": "SStrauss",
        "full_name": "Stefan Strauss",
        "user_name": "hmpftata",
        "location": "Vienna, Austria",
        "primary_activity": "CYCLING",
        "cycling_max_avg_power": 250,
        "user_level": 12,
    }