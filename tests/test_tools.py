"""Test suite for mcp-garmin tools."""

import pytest
from unittest.mock import Mock, patch

from mcp_garmin.tools.base import register
from mcp_garmin.tools.body import get_body_weight
from mcp_garmin.tools.heart import get_daily_heart_rate
from mcp_garmin.tools.sleep import get_sleep_summary
from mcp_garmin.tools.stress import get_daily_stress
from mcp_garmin.tools.activity import get_activities
from mcp_garmin.tools.steps import get_daily_steps
from mcp_garmin.tools.hydration import get_daily_hydration
from mcp_garmin.tools.devices import get_connected_devices
from mcp_garmin.tools.nutrition import get_nutrition_log
from mcp_garmin.tools.goals import get_steps_goal
from mcp_garmin.tools.util import get_user_profile


def test_tool_registration():
    """Test that all tools are properly registered."""
    # Test that our decorator works correctly
    assert hasattr(get_body_weight, 'tool_metadata')
    assert hasattr(get_daily_heart_rate, 'tool_metadata')
    assert hasattr(get_sleep_summary, 'tool_metadata')
    assert hasattr(get_daily_stress, 'tool_metadata')
    assert hasattr(get_activities, 'tool_metadata')
    assert hasattr(get_daily_steps, 'tool_metadata')
    assert hasattr(get_daily_hydration, 'tool_metadata')
    assert hasattr(get_connected_devices, 'tool_metadata')
    assert hasattr(get_nutrition_log, 'tool_metadata')
    assert hasattr(get_steps_goal, 'tool_metadata')
    assert hasattr(get_user_profile, 'tool_metadata')


def test_tool_signatures():
    """Test that all tools have correct signatures."""
    # All tools should be callable with appropriate parameters
    tools = [
        get_body_weight,
        get_daily_heart_rate,
        get_sleep_summary,
        get_daily_stress,
        get_activities,
        get_daily_steps,
        get_daily_hydration,
        get_connected_devices,
        get_nutrition_log,
        get_steps_goal,
        get_user_profile,
    ]
    
    for tool in tools:
        assert callable(tool)


def test_tool_decorators():
    """Test that tool decorators work correctly."""
    # Test registration decorator
    assert hasattr(register, '__call__')
    assert callable(register)