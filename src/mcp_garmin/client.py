"""Token handling + casing + error cascade for the Garmin API."""
from __future__ import annotations

from collections.abc import Callable
from functools import wraps
from typing import Any

import garth
from garth.exc import GarthException
from garth.storage import FileTokenStorage
from garth.utils import asdict

_TOKEN_DIR = "~/.garth"
_client: garth.http.Client | None = None


class ToolError(Exception):
    """Returned to MCP tools when a Garmin API error occurs."""


def get_client() -> garth.http.Client:
    """Load token from ~/.garth/ and return the cached garth client."""
    global _client
    if _client is not None:
        return _client
    c = garth.http.client
    c.storage = FileTokenStorage(_TOKEN_DIR)
    c.oauth2_token = c.storage.load()
    _client = c
    return c


def _to_dict(obj: Any) -> dict:
    """Serialize a Garmin API object to a JSON-serializable dict (snake_case)."""
    if obj is None:
        return {}
    if isinstance(obj, dict):
        return obj
    return asdict(obj)


def _handle_garmin_error(func: Callable) -> Callable:
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
