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
        c = garth.http.client  # _auto_resume() loads from GARTH_HOME
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
