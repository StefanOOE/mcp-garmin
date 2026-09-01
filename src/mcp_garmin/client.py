"""Token-Handling + Casing + Fehler-Kaskade für Garmin API."""
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
    """Wird an MCP-Tools zurückgegeben wenn Garmin-API-Fehler auftreten."""


def get_client() -> garth.http.Client:
    """Lädt Token aus ~/.garth/ und gibt den garth Client zurück. Cached."""
    global _client
    if _client is not None:
        return _client
    c = garth.http.client
    c.storage = FileTokenStorage(_TOKEN_DIR)
    c.oauth2_token = c.storage.load()
    _client = c
    return c


def _to_dict(obj: Any) -> dict:
    """Serialisiert ein Garmin-API-Objekt zu einem JSON-serialisierbaren dict (snake_case)."""
    if obj is None:
        return {}
    if isinstance(obj, dict):
        return obj
    return asdict(obj)


def _handle_garmin_error(func: Callable) -> Callable:
    """Decorator: fängt GarthException ab und wirft ToolError mit deutscher Meldung."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except GarthException as e:
            msg = str(e)
            if "token" in msg.lower():
                raise ToolError(
                    f"Garmin-Token-Fehler: {msg}. "
                    "Token abgelaufen — .venv/bin/python garmin_login.py ausführen."
                ) from e
            raise ToolError(f"Garmin-API-Fehler: {msg}") from e

    return wrapper
