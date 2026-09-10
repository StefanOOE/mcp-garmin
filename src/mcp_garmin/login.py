#!/usr/bin/env python3
# Garmin login for mcp-garmin (garth 0.8.0).
# Sets GARTH_HOME so garth auto-persists both oauth1_token.json and
# oauth2_token.json under ~/.garth/. The MCP server uses the same GARTH_HOME
# to auto-resume the session.
import getpass
import os
import sys


def main() -> int:
    # Must be set before first access to garth.http.client so _auto_resume()
    # knows where to load/dump tokens.
    os.environ["GARTH_HOME"] = os.path.expanduser("~/.garth")
    import garth

    email = "garmin.com.ploy864@passmail.net"
    password = getpass.getpass("Garmin password: ")
    garth.login(email, password)  # auto-dumps oauth1 + oauth2 to GARTH_HOME

    try:
        profile = garth.UserProfile.get()
        actual = profile.user_name if hasattr(profile, "user_name") else str(profile)
        print(f"Verified: profile '{actual}' accessible")
    except Exception as exc:
        print(f"Login ok, but verification failed: {exc}")
        return 1
    print("mcp-garmin is ready to go.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
