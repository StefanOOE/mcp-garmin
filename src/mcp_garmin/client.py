"""Garmin client + token handling for garth-ng 1.1.0.

Two complementary APIs live here so the mid-migration codebase stays importable:

* ``GarminClient`` -- the injectable singleton (concept §3.1) used by ``tools/*``
  and the unit tests. Wraps the ``garth.http.Client`` singleton, guarantees a
  valid session (GARTH_HOME resume + refresh), and exposes the ``_to_dict`` /
  ``_handle_garmin_error`` helpers.
* Module-level ``get_client`` / ``_to_dict`` / ``_handle_garmin_error`` /
  ``ToolError`` / ``FileTokenStorage`` -- the legacy surface that the root tool
  modules (``activity``, ``body``, ``sleep`` ...) still import. The module
  functions delegate to a shared ``GarminClient`` so both layers share one
  session.

Token state is read from the real ``garth.http.Client.oauth2_token``. Garth-ng
resumes tokens itself via ``Client._auto_resume`` from ``GARTH_HOME``, but the
singleton is constructed at ``import garth.http`` time -- i.e. *before* this
module (or ``login.py``) sets ``GARTH_HOME`` -- so ``get_client()`` performs an
explicit ``Client.load(GARTH_HOME)`` to resume a token that was never loaded.

``FileTokenStorage`` is a small legacy shim (the ``garth.storage`` module does
not exist in garth-ng 1.1.0); it is only used to satisfy the legacy
``get_client()`` contract and is mockable in tests.
"""

from __future__ import annotations

import os
from collections.abc import Callable
from functools import wraps
from typing import TYPE_CHECKING, Any

import garth
from garth.exc import GarthException
from garth.utils import asdict

from .errors import TokenError, ToolError

if TYPE_CHECKING:
    from garth.http import Client

try:  # garth 0.x had garth.storage.FileTokenStorage; garth-ng 1.1.0 does not.
    from garth.storage import FileTokenStorage  # type: ignore[attr-defined]
except ModuleNotFoundError:  # pragma: no cover - ng path

    class FileTokenStorage:  # type: ignore[no-redef]
        """Legacy token storage shim (garth 0.x API).

        Garth-ng resumes tokens itself via ``Client._auto_resume`` from
        ``GARTH_HOME``; this shim exists only so the legacy ``get_client()``
        contract (``c.storage = FileTokenStorage(dir); c.oauth2_token =
        c.storage.load()``) keeps working and stays mockable.
        """

        def __init__(self, directory: str) -> None:
            self.directory = directory

        def load(self) -> Any:
            try:
                import json
                import pathlib

                path = pathlib.Path(self.directory) / "oauth2_token.json"
                if path.exists():
                    return json.loads(path.read_text())
            except OSError:
                return None
            return None


# Default token directory (overridable via GARTH_HOME). Not a secret — the
# OAuth2/refresh tokens live in files under this dir, so B105 is a false
# positive here.
_TOKEN_DIR = "~/.garth"  # nosec: B105

# Module-level singleton client (legacy cache + shared session for tools/*).
_client: Client | None = None

# Shared GarminClient instance backing the module-level facade.
_instance: GarminClient | None = None


def _token_dir() -> str:
    return os.path.expanduser(_TOKEN_DIR)


def _ensure_garth_home() -> None:
    """Point GARTH_HOME at ~/.garth before touching the garth singleton.

    Must happen before ``garth.http.client`` is first accessed so that
    ``Client._auto_resume`` knows where to load the OAuth2 token from.
    """
    os.environ.setdefault("GARTH_HOME", _token_dir())


def _resume_token(c: Any) -> None:
    """Load a persisted token into ``c`` from ``GARTH_HOME`` (no-op if present).

    The garth-ng singleton is built at import time, before ``GARTH_HOME`` is
    set, so a token that was never loaded stays ``None``. Resume it here when a
    token file exists. Raises ``GarthException`` if the dir has no token file
    (or holds a legacy OAuth1 token) -- the caller maps that to ``TokenError``.
    """
    if getattr(c, "oauth2_token", None) is not None:
        return
    home = os.environ.get("GARTH_HOME") or _token_dir()
    if os.path.exists(os.path.join(os.path.expanduser(home), "oauth2_token.json")):
        c.load(home)


def _singleton() -> Client:
    """Return the garth-ng ``Client`` singleton with a valid session.

    Raises ``TokenError`` if no usable token exists (run the login).
    """
    global _client
    if _client is not None:
        return _client
    _ensure_garth_home()
    c = garth.http.client  # _auto_resume() runs at import; may be empty
    _resume_token(c)
    if getattr(c, "oauth2_token", None) is None:
        raise TokenError(
            "No valid Garmin token. Run the login to authenticate "
            "(e.g. .venv/bin/python -m mcp_garmin.login)."
        )
    _client = c
    return c


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
    """Single Garmin session per process. Injectable for tests."""

    def __init__(self, garth_client: Client | None = None) -> None:
        self._garth_client = garth_client

    def get_client(self) -> Client:
        """Return a valid garth session (GARTH_HOME resume + refresh).

        Raises ``TokenError`` if no usable token exists (run ``login.py``).
        """
        if self._garth_client is not None:
            return self._garth_client
        return _singleton()

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

    def _to_dict(self, obj: Any) -> dict:
        """Serialize a Garmin object to a JSON-serializable dict.

        ``dict``s pass through unchanged, ``None`` -> ``{}``, everything else
        goes through ``garth.utils.asdict`` (dataclass -> snake_case dict).
        """
        if obj is None:
            return {}
        if isinstance(obj, dict):
            return obj
        return asdict(obj)

    def _handle_garmin_error(self, func: Callable) -> Callable:
        """Decorator: map ``garth.exc.GarthException`` -> ToolError/TokenError.

        Delegates to ``errors.from_garmin`` so token problems are recognised by
        exception type (``AuthenticationError``/``refresh_expired``), not just a
        substring match. Non-Garth exceptions pass through unchanged.
        """

        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                return func(*args, **kwargs)
            except GarthException as e:
                raise _from_garmin(e) from e

        return wrapper

    # -- convenience pass-throughs (legacy tools use get/list) -------------
    def get(self, *args: Any, **kwargs: Any) -> Any:
        return self.get_client().get(*args, **kwargs)

    def list(self, *args: Any, **kwargs: Any) -> Any:
        return self.get_client().list(*args, **kwargs)


# ---------------------------------------------------------------------------
# Module-level facade (legacy API)
# ---------------------------------------------------------------------------


def _from_garmin(exc: GarthException) -> ToolError:
    """Map a garth exception to ToolError/TokenError (via errors.from_garmin)."""
    from .errors import from_garmin

    return from_garmin(exc)


def get_client() -> Client:
    """Return the shared garth-ng client (cached). Raises TokenError if not logged in.

    Legacy contract: ``c.storage = FileTokenStorage(dir)`` then
    ``c.oauth2_token = c.storage.load()``. Garth-ng has no ``garth.storage``
    module, so ``FileTokenStorage`` is a thin shim that reads the same
    ``oauth2_token.json`` file garth-ng persists.
    """
    global _client, _instance
    if _client is not None:
        return _client
    _ensure_garth_home()
    if _instance is None:
        _instance = GarminClient()
    c = garth.http.client  # _auto_resume() may already have loaded the token
    c.storage = FileTokenStorage(_token_dir())
    c.oauth2_token = c.storage.load()
    if c.oauth2_token is None:
        _resume_token(c)  # fall back to garth's own loader (handles OAuth1)
    if getattr(c, "oauth2_token", None) is None:
        try:
            c.refresh_token()  # last-chance: refresh a not-yet-loaded token
        except GarthException as e:
            raise _from_garmin(e) from e
    _client = c
    return c


def _to_dict(obj: Any) -> dict:
    """Serialize a Garmin API object to a JSON-serializable dict (snake_case)."""
    global _instance
    if _instance is None:
        _instance = GarminClient()
    return _instance._to_dict(obj)


def _handle_garmin_error(func: Callable) -> Callable:
    """Decorator: catch ``GarthException`` and raise ``ToolError``/``TokenError``."""
    global _instance
    if _instance is None:
        _instance = GarminClient()
    return _instance._handle_garmin_error(func)


__all__ = [
    "FileTokenStorage",
    "GarminClient",
    "TokenError",
    "ToolError",
    "_handle_garmin_error",
    "_to_dict",
    "asdict",
    "get_client",
]