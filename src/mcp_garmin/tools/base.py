"""Base classes and registry for MCP tools."""

from __future__ import annotations

from typing import Any, Callable, Dict, List

# Registry to store registered tools
_TOOL_REGISTRY: Dict[str, Any] = {}


def register(func: Callable[..., Any]) -> Callable[..., Any]:
    """Decorator to register a tool function."""
    _TOOL_REGISTRY[func.__name__] = func
    return func


def get_registered_tools() -> List[Any]:
    """Get all registered tools."""
    return list(_TOOL_REGISTRY.values())


def get_tool_names() -> List[str]:
    """Get all registered tool names."""
    return list(_TOOL_REGISTRY.keys())