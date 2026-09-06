#!/usr/bin/env python3
# One-time Garmin login for mcp-garmin (garth-ng 2.0.0a1).
# Stores the token as JSON under ~/.garth/oauth2_token.json and verifies
# with a real API call. The MCP process must then be started with the
# same HOME (default: /home/ss).
import getpass
import json
import os
import sys
from pathlib import Path
import garth
from garth.storage import FileTokenStorage, OAUTH2_TOKEN_FILE


def save_token(token, path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)
    target = path / OAUTH2_TOKEN_FILE
    payload = garth.utils.asdict(token) if hasattr(garth, "utils") else None
    if payload is None:
        from garth.utils import asdict
        payload = asdict(token)
    target.write_text(json.dumps(payload, indent=4))
    os.chmod(target, 0o600)
    print(f"Token saved to {target}")


def verify(username: str) -> None:
    profile = garth.UserProfile.get()
    actual = profile.get("userName", "?") if isinstance(profile, dict) else "?"
    print(f"Verified: profile '{actual}' accessible")


def main() -> int:
    email = input("Garmin email: ").strip()
    password = getpass.getpass("Garmin password: ")
    token = garth.login(email, password)
    save_token(token, Path(os.path.expanduser("~/.garth")))
    try:
        verify(email)
    except Exception as exc:  # noqa: BLE001
        print(f"Login ok, but verification failed: {exc}")
        return 1
    print("mcp-garmin is ready to go.")
    return 0


if __name__ == "__main__":
    sys.exit(main())