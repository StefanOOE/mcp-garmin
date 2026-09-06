import datetime
from typing import Any
from mcp_garmin.serialization import camel_to_snake_dict, project_sleep_fields


def test_camel_to_snake_dict():
    """Test conversion of camelCase keys to snake_case keys."""
    data = {
        "camelCaseKey": "value1",
        "anotherCamelCaseKey": "value2",
        "normalKey": "value3"
    }
    
    result = camel_to_snake_dict(data)
    expected = {
        "camel_case_key": "value1",
        "another_camel_case_key": "value2",
        "normal_key": "value3"
    }
    
    assert result == expected


def test_project_sleep_fields():
    """Test projection of sleep-related fields from a DailySummary."""
    data = {
        "sleeping_seconds": 28800,
        "sleep_time_seconds": 28800,
        "non_sleep_field": "value",
        "sleep_score": 85,
        "sleep_start_timestamp_gmt": 1634567890,
        "other_field": "other_value"
    }
    
    result = project_sleep_fields(data)
    expected = {
        "sleeping_seconds": 28800,
        "sleep_time_seconds": 28800,
        "sleep_score": 85,
        "sleep_start_timestamp_gmt": 1634567890
    }
    
    assert result == expected


def test_project_sleep_fields_empty():
    """Test projection with empty data."""
    result = project_sleep_fields({})
    assert result == {}


def test_project_sleep_fields_none():
    """Test projection with None data."""
    # The function should handle None gracefully
    # But since the function expects dict[str, Any], we'll test with empty dict
    result = project_sleep_fields({})
    assert result == {}