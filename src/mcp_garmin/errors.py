"""Error handling for Garmin tools."""

from __future__ import annotations


from garth.exc import GarthException


class ToolError(Exception):
    """Raised by tools when a Garmin API error occurs."""


class TokenError(ToolError):
    """Raised when the Garmin token is invalid/expired."""


def from_garmin(exc: GarthException) -> ToolError:
    """Convert a Garmin exception to a ToolError."""
    msg = str(exc)
    if "token" in msg.lower():
        return TokenError(
            f"Garmin token error: {msg}. "
            "Token expired — run .venv/bin/python garmin_login.py."
        )
    return ToolError(f"Garmin API error: {msg}")
