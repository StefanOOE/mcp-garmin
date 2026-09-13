"""This module provides a client for interacting with the Garmin API using the Garth library."""
import os
import logging
from datetime import date
from dotenv import load_dotenv
import garth
from garth.exc import GarthException

load_dotenv()

log = logging.getLogger(__name__)

def login() -> None:
    """Resume or establish a Garth session for API authentication."""
    try:
        garth.resume("~/.garth")
        log.info("Resuming Garth session")
        return
    except GarthException as exc:
        log.info("Garth error resuming Garth session: %s", exc)

    try:
        garth.login(os.getenv("GARMIN_USERNAME"), os.getenv("GARMIN_PASSWORD"))
    except GarthException as exc:
        log.error("Garth error logging in to Garth: %s", exc)
        raise

    log.info("Successfully logged in to Garth")
    garth.save("~/.garth")

def get_sleep_data(target_date: date) -> garth.SleepData | None:
    """Retrieve sleep data for the specified date using Garth API."""
    try:
        login()
        result = garth.SleepData.get(target_date)
        return result
    except GarthException as exc:
        log.error("Garth error getting sleep data: %s", exc)
        raise
