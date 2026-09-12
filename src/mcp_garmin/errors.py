"""Error mapping for Garmin tools (garth-ng 1.1.0).

Maps the ``garth.exc`` hierarchy onto two tool-facing exceptions:

- ``ToolError``   — a Garmin API failure (rate limit, Cloudflare, generic).
- ``TokenError``  — a token problem (missing/invalid/expired); the operator
  should re-run ``mcp-garmin-login``.

``from_garmin`` is the single entry point used by
``GarminClient._handle_garmin_error`` so every tool gets identical mapping.
No bare ``except`` is used; each branch keys on exception type or an explicit
HTTP status.
"""

from __future__ import annotations


from garth.exc import (
    AuthenticationError,
    CloudflareError,
    GarthException,
    GarthHTTPError,
    MFARequiredError,
    RateLimitError,
)

__all__ = ["TokenError", "ToolError", "from_garmin"]

_LOGIN_HINT = "Run mcp-garmin-login to re-authenticate."

# Token-path phrases recognised when garth-ng raises a *plain*
# ``GarthException`` (no dedicated subclass). The ``oauth2 token`` /
# ``oauth2token`` pair, ``legacy oauth1 tokens``, ``no token files found``
# and ``token format`` are the literal token-path messages emitted by
# ``Client.request(api=True)``, ``Client.refresh_token()`` and
# ``Client.load()`` (verified against the installed garth-ng 1.1.0).
# ``token expired`` is an unambiguous token problem phrase (not the bare
# substring ``"token"``, which the concept deliberately avoids) kept for
# compatibility with the legacy tool surface.
_TOKEN_MARKERS = (
    "oauth2 token",
    "oauth2token",
    "legacy oauth1 tokens",
    "no token files found",
    "token format",
    "token expired",
)


class ToolError(Exception):
    """Raised by tools when a Garmin API error occurs."""


class TokenError(ToolError):
    """Raised when the Garmin token is missing, invalid, or expired."""


def _token_error(exc: GarthException) -> TokenError:
    return TokenError(f"Garmin token error: {exc}. {_LOGIN_HINT}")


def _http_status(exc: GarthException) -> int | None:
    """Best-effort HTTP status from a ``GarthHTTPError`` (else ``None``)."""
    if not isinstance(exc, GarthHTTPError):
        return None
    response = getattr(exc.error, "response", None)
    status = getattr(response, "status_code", None)
    return status if isinstance(status, int) else None


def from_garmin(exc: GarthException) -> ToolError:
    """Map a garth-ng exception to ``ToolError``/``TokenError``.

    Token problems are recognised by exception type (``AuthenticationError``,
    ``MFARequiredError``) or by the token-expiry messages garth-ng emits as a
    plain ``GarthException`` — not by the substring ``"token"`` alone.
    """
    if isinstance(exc, (AuthenticationError, MFARequiredError)):
        return _token_error(exc)

    msg = str(exc)
    lowered = msg.lower()
    if any(marker in lowered for marker in _TOKEN_MARKERS):
        return _token_error(exc)

    status = _http_status(exc)
    if isinstance(exc, RateLimitError) or status == 429:
        return ToolError(f"Garmin rate-limited; retry later. ({msg})")

    if isinstance(exc, CloudflareError) or status == 403:
        return ToolError(f"Cloudflare challenge; check network/UA. ({msg})")

    if status == 401:
        return _token_error(exc)

    return ToolError(f"Garmin API error: {msg}")
