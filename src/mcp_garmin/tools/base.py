"""Base classes and registry for MCP tools."""

from __future__ import annotations

from typing import Any, Callable, Dict, List
from functools import wraps
import garth
from garth.exc import GarthException
from garth.utils import asdict
import os


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


def _secure_token_perms() -> None:
    """Ensure secure permissions for GARTH_HOME directory and token files.
    
    Sets directory permissions to 0o700 and token file permissions to 0o600.
    Ignores FileNotFoundError/OSError to avoid breaking tools.
    """
    try:
        # Ensure GARTH_HOME directory has secure permissions (0o700)
        garth_home = os.path.expanduser("~/.garth")
        os.makedirs(garth_home, exist_ok=True)
        os.chmod(garth_home, 0o700)
        
        # Secure the token file permissions (0o600)
        token_file = os.path.join(garth_home, "oauth2_token.json")
        os.chmod(token_file, 0o600)
    except (FileNotFoundError, OSError):
        # Ignore permission errors to avoid breaking tools
        pass


class GarminClient:
    """Thin GarminClient wrapper around garth session with dependency injection."""
    
    def __init__(self, garth_client: garth.http.Client | None = None) -> None:
        """Initialize GarminClient with optional injected garth client."""
        self._garth_client = garth_client
        # Token storage is handled differently in newer garth versions
        self._token_dir = os.path.expanduser("~/.garth")
    
    def get_client(self) -> garth.http.Client:
        """Get or create a garth client with token persistence."""
        if self._garth_client is not None:
            return self._garth_client
        
        global _client
        if _client is not None:
            return _client
        
        # Ensure GARTH_HOME is set so garth auto-loads both tokens.
        os.environ.setdefault("GARTH_HOME", self._token_dir)
        # Set telemetry default for defense-in-depth
        os.environ.setdefault("GARTH_TELEMETRY_ENABLED", "false")
        c = garth.http.client  # _auto_resume() loads from GARTH_HOME
        
        # Apply secure permissions after client creation
        _secure_token_perms()
        
        _client = c
        return c
    
    def _to_dict(self, obj: Any) -> dict:
        """Serialize a Garmin API object to a JSON-serializable dict (snake_case)."""
        if obj is None:
            return {}
        if isinstance(obj, dict):
            return obj
        return asdict(obj)
    
    def _handle_garmin_error(self, func: Callable) -> Callable:
        """Decorator: catches GarthException and raises ToolError with a descriptive message."""

        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except GarthException as e:
                msg = str(e)
                if "token" in msg.lower():
                    raise ToolError(
                        f"Garmin token error: {msg}. "
                        "Token expired — run .venv/bin/python garmin_login.py."
                    ) from e
                raise ToolError(f"Garmin API error: {msg}") from e
        
        return wrapper
    
    def get(self, *args, **kwargs) -> Any:
        """Pass-through to garth client get method."""
        client = self.get_client()
        return client.get(*args, **kwargs)
    
    def list(self, *args, **kwargs) -> Any:
        """Pass-through to garth client list method."""
        client = self.get_client()
        return client.list(*args, **kwargs)
    
    def refresh(self) -> None:
        """Refresh the Garmin client token and secure permissions."""
        client = self.get_client()
        # Refresh the token using garth's refresh mechanism
        # This ensures that when garth persists the new token internally,
        # we apply secure permissions afterwards
        try:
            # Call refresh_token on the garth client
            client.refresh_token()
            # Apply secure permissions after refresh
            _secure_token_perms()
        except Exception:
            # If refresh fails, still try to secure existing tokens
            _secure_token_perms()


# Global client instance
_client: garth.http.Client | None = None


# Module-level functions for backward compatibility
def get_client() -> garth.http.Client:
    """Get or create a garth client with token persistence."""
    gc = GarminClient()
    return gc.get_client()


def _to_dict(obj: Any) -> dict:
    """Serialize a Garmin API object to a JSON-serializable dict (snake_case)."""
    gc = GarminClient()
    return gc._to_dict(obj)


def _handle_garmin_error(func: Callable) -> Callable:
    """Decorator: catches GarthException and raises ToolError with a descriptive message."""
    gc = GarminClient()
    return gc._handle_garmin_error(func)


class ToolError(Exception):
    """Raised by tools when a Garmin API error occurs."""