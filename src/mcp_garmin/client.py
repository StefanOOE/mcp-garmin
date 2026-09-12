"""Client and token handling for Garmin API."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Callable
from functools import wraps
import os
import garth

from garth.exc import GarthException
from garth.utils import asdict

if TYPE_CHECKING:
    from garth.http import Client


_TOKEN_DIR = "~/.garth"
_client: garth.http.Client | None = None


class ToolError(Exception):
    """Raised by tools when a Garmin API error occurs."""


def _secure_token_perms() -> None:
    """Ensure secure permissions for GARTH_HOME directory and token files.
    
    Sets directory permissions to 0o700 and token file permissions to 0o600.
    Ignores FileNotFoundError/OSError to avoid breaking tools.
    """
    try:
        # Ensure GARTH_HOME directory has secure permissions (0o700)
        garth_home = os.path.expanduser(os.environ.get("GARTH_HOME", _TOKEN_DIR))
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

    def __init__(self, garth_client: Client | None = None) -> None:
        """Initialize GarminClient with optional injected garth client."""
        self._garth_client = garth_client
        # Token storage is handled differently in newer garth versions
        self._token_dir = os.path.expanduser(_TOKEN_DIR)

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
