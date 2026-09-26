"""Shared functions and utilities for Garmin tools."""
from datetime import datetime, timezone
from functools import singledispatch

@singledispatch
def local_iso(timestamp) -> str:
    """Convert a Garmin timestamp or a *_timestamp_local epoch-ms field to an ISO string.

    Garmin's API has no version field to detect a renamed/missing key against
    (see README disclaimer), so this degrades to "unknown" instead of crashing
    the whole tool if the field is ever absent.
    """
    if timestamp is None:
        return "unknown"
    raise TypeError(f"Unsupported type: {type(timestamp)}")

@local_iso.register
def _(timestamp: int) -> str:
    """Convert *_timestamp_local epoch-ms field to an ISO-8601 string."""
    local_dt = datetime.fromtimestamp(timestamp / 1000, tz=timezone.utc)
    return local_dt.replace(tzinfo=None).isoformat()

@local_iso.register
def _(timestamp: datetime) -> str:
    """Convert a datetime value to an ISO-8601 string.

    When a field is already typed as datetime upstream (e.g. garth's HRVData),
    it arrives *naive* (no tzinfo) but already represents the correct local
    wall-clock time - unlike the int overload above, no conversion is needed
    here, only formatting. Verified empirically: astimezone(utc) on this value
    incorrectly shifts it by the host machine's timezone offset, because a
    naive datetime is presumed by Python to be in the system's local zone.
    """
    return timestamp.replace(tzinfo=None).isoformat()

def grams_to_kg(grams: float | None) -> float | None:
    """Convert a Garmin gram value to kilograms, passing None through unchanged."""
    return grams / 1000 if grams is not None else None
