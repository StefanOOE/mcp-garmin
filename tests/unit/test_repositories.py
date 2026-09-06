"""Unit tests for GarminRepository."""

import pytest
from unittest.mock import Mock, patch, MagicMock

from mcp_garmin.repositories import GarminRepository
from mcp_garmin.errors import ToolError


def test_repository_initialization():
    """Test GarminRepository initialization."""
    repo = GarminRepository()
    assert repo is not None


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
        'morning_training_readiness',
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


@patch('mcp_garmin.repositories.garth')
@patch('mcp_garmin.repositories.asdict')
def test_weight_method(mock_asdict, mock_garth):
    """Test weight method."""
    # Setup mocks
    mock_client = Mock()
    mock_garth.data.WeightData.get.return_value = "mock_result"
    mock_asdict.return_value = {"weight": 70000}
    
    # Test
    repo = GarminRepository(mock_client)
    result = repo.weight(day="2023-01-01")
    
    # Verify
    assert result == {"weight": 70000}
    mock_garth.data.WeightData.get.assert_called_once_with(day="2023-01-01", client=mock_client)


@patch('mcp_garmin.repositories.garth')
@patch('mcp_garmin.repositories.asdict')
def test_sleep_method(mock_asdict, mock_garth):
    """Test sleep method."""
    # Setup mocks
    mock_client = Mock()
    mock_garth.SleepData.get.return_value = "mock_result"
    mock_asdict.return_value = {"sleep_data": "test"}
    
    # Test
    repo = GarminRepository(mock_client)
    result = repo.sleep(day="2023-01-01")
    
    # Verify
    assert result == {"sleep_data": "test"}
    mock_garth.SleepData.get.assert_called_once_with(day="2023-01-01", client=mock_client)


@patch('mcp_garmin.repositories.garth')
def test_device_info_method(mock_garth):
    """Test device_info method with fallback."""
    # Setup mocks
    mock_client = Mock()
    mock_garth.http.Client().connectapi.side_effect = Exception("API Error")
    mock_garth.data.UserProfile.get.return_value = {"device_type": "watch"}
    
    # Test
    repo = GarminRepository(mock_client)
    result = repo.device_info()
    
    # Verify
    assert result == {"device_type": "watch"}


@patch('mcp_garmin.repositories.GarthException')
def test_error_handling(mock_garth_exception):
    """Test error handling in repository methods."""
    # Setup mocks
    mock_client = Mock()
    mock_client.connectapi.side_effect = mock_garth_exception
    
    # Test
    repo = GarminRepository(mock_client)
    
    # Should raise ToolError
    with pytest.raises(ToolError):
        repo.device_info()


def test_method_signatures():
    """Test that methods have correct signatures."""
    repo = GarminRepository()
    
    # Check a few methods for proper signature
    import inspect
    
    # weight method
    sig = inspect.signature(repo.weight)
    assert 'day' in sig.parameters
    assert sig.parameters['day'].default is None
    
    # weight_history method  
    sig = inspect.signature(repo.weight_history)
    assert 'end' in sig.parameters
    assert 'days' in sig.parameters
    assert sig.parameters['days'].default == 7
    
    # sleep method
    sig = inspect.signature(repo.sleep)
    assert 'day' in sig.parameters
    assert sig.parameters['day'].default is None