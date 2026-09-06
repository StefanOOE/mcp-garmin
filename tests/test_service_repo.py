"""Test suite for mcp-garmin service and repository."""

import pytest
from unittest.mock import Mock, patch

from mcp_garmin.repositories import GarminRepository
from mcp_garmin.garmin_service import GarminService


def test_repository_initialization():
    """Test GarminRepository initialization."""
    repo = GarminRepository()
    assert repo is not None


def test_service_initialization():
    """Test GarminService initialization."""
    service = GarminService()
    assert service is not None


def test_repository_methods_exist():
    """Test that all expected repository methods exist."""
    repo = GarminRepository()
    
    expected_methods = [
        'weight',
        'weight_history',
        'blood_pressure',
        'body_battery',
        'body_battery_stress',
        'body_battery_stress_history',
        'daily_heart_rate',
        'hrv',
        'resting_heart_rate',
        'sleep',
        'sleep_detail',
        'sleep_summary',
        'daily_stress',
        'weekly_stress',
        'training_status_daily',
        'training_status_weekly',
        'training_status_monthly',
        'training_readiness',
        'activities',
        'activity_detail',
        'activity_map',
        'fitness_activities',
        'personal_records',
        'personal_record_types',
        'daily_steps',
        'weekly_steps',
        'daily_summary',
        'daily_summary_history',
        'daily_hydration',
        'hydration_history',
        'device_info',
        'connected_devices',
        'nutrition_log',
        'nutrition_status',
        'steps_goal',
        'weight_goal',
        'garmin_scores',
        'user_profile',
        'user_settings',
    ]
    
    for method in expected_methods:
        assert hasattr(repo, method), f"Repository missing method: {method}"


def test_service_methods_exist():
    """Test that all expected service methods exist."""
    service = GarminService()
    
    expected_methods = [
        'get_body_weight',
        'get_blood_pressure',
        'get_body_battery',
        'get_body_battery_stress',
        'get_daily_heart_rate',
        'get_hrv',
        'get_resting_heart_rate',
        'get_sleep',
        'get_sleep_detail',
        'get_sleep_summary',
        'get_daily_stress',
        'get_training_status_daily',
        'get_training_readiness',
        'get_activities',
        'get_activity_detail',
        'get_activity_map',
        'get_fitness_activities',
        'get_personal_records',
        'get_personal_record_types',
        'get_daily_steps',
        'get_weekly_steps',
        'get_daily_summary',
        'get_daily_hydration',
        'get_hydration_history',
        'get_device_info',
        'get_connected_devices',
        'get_nutrition_log',
        'get_nutrition_status',
        'get_steps_goal',
        'get_weight_goal',
        'get_garmin_scores',
        'get_user_profile',
        'get_user_settings',
    ]
    
    for method in expected_methods:
        assert hasattr(service, method), f"Service missing method: {method}"