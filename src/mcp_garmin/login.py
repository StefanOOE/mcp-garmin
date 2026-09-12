#!/usr/bin/env python3
# Garmin login for mcp-garmin (garth-ng 1.1.0).
# Sets GARTH_HOME so garth auto-persists both oauth1_token.json and
# oauth2_token.json under ~/.garth/. The MCP server uses the same GARTH_HOME
# to auto-resume the session.
import getpass
import os
import sys

from garth.exc import GarthException

def main() -> int:
    # Must be set before first access to garth.http.client so _auto_resume()
    # knows where to load/dump tokens.
    os.environ["GARTH_HOME"] = os.path.expanduser("~/.garth")
    import garth
    
    email = os.environ.get("GARMIN_EMAIL") or input("Garmin email: ")
    password = getpass.getpass("Garmin password: ")
    
    # Try regular login first
    try:
        garth.login(email, password)
    except GarthException as e:
        # Check if it's an MFA-related error and try again with MFA
        error_str = str(e).lower()
        if "mfa" in error_str or "two-factor" in error_str or "otp" in error_str:
            print("MFA authentication required")
            mfa_code = input("Enter MFA code: ")
            garth.login(email, password, mfa_code)
        elif "invalid" in error_str or "credential" in error_str:
            # Invalid credentials - re-prompt
            print("Invalid credentials, please try again")
            return 1
        else:
            # Re-raise other GarthException
            raise
    except OSError as e:
        # Handle OS-related errors specifically
        print(f"OS error during login: {e}")
        return 1
    
    # Secure token permissions after login
    from mcp_garmin.client import _secure_token_perms
    _secure_token_perms()
    
    try:
        profile = garth.UserProfile.get()
        actual = profile.user_name if hasattr(profile, "user_name") else str(profile)
        print(f"Verified: profile '{actual}' accessible")
    except GarthException as e:
        print(f"Login ok, but verification failed: {e}")
        return 1
    except OSError as e:
        print(f"OS error during verification: {e}")
        return 1
    print("mcp-garmin is ready to go.")
    return 0


if __name__ == "__main__":
    sys.exit(main())