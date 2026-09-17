"""This module provides a client for interacting with the Garmin API using the Garth library."""
import logging
from datetime import date
import garth
from garth.exc import GarthException
import config

log = logging.getLogger(__name__)

def login() -> None:
    """Resume or establish a Garth session for API authentication."""
    try:
        garth.resume(config.GARTH_SESSION_DIR)
        log.info("Resuming Garth session")
        return
    except GarthException as exc:
        log.info("Garth error resuming Garth session: %s", exc)

    try:
        garth.login(config.GARMIN_USERNAME, config.GARMIN_PASSWORD)
    except GarthException as exc:
        log.error("Garth error logging in to Garth: %s", exc)
        raise

    log.info("Successfully logged in to Garth")
    garth.save(config.GARTH_SESSION_DIR)

def get_sleep_data(target_date: date) -> garth.SleepData | None:
    """Retrieve sleep data for the specified date using Garth API."""
    try:
        login()
        raw = garth.SleepData.get(target_date)
        return raw
    except GarthException as exc:
        log.error("Garth error getting sleep data: %s", exc)
        raise

def get_hrv_data(target_date: date) -> garth.HRVData | None:
    """Retrieve heart rate variability (HRV) data for the specified date using Garth API."""
    try:
        login()
        raw = garth.HRVData.get(target_date)
        return raw
    except GarthException as exc:
        log.error("Garth error getting HRV data: %s", exc)
        raise

def get_activities(date_from: date, period: int) -> list[tuple[int, date, str]]:
    """Retrieve a list of available activities (activity_id, date, type) using Garth API."""
    try:
        login()
        raw = garth.FitnessActivity.list(date_from, period)
        return [(act.activity_id, act.start_local, act.activity_type) for act in raw]
    except GarthException as exc:
        log.error("Garth error getting fitness activity data: %s", exc)
        raise

def get_activity_detail(activity_id: int) -> garth.Activity | None:
    """Retrieve activity data for a specific activity ID using Garth API."""
    try:
        login()
        raw = garth.Activity.get(activity_id)
        return raw
    except GarthException as exc:
        log.error("Garth error getting activity data for id %d: %s", activity_id, exc)
        raise

def get_steps_data(target_date: date, period: int) -> list[garth.DailySteps]:
    """Retrieve daily step counts for the specified date and period using Garth API."""
    try:
        login()
        raw = garth.DailySteps.list(target_date, period)
        return raw
    except GarthException as exc:
        log.error("Garth error getting steps data: %s", exc)
        raise

def get_weight_data(target_date: date) -> garth.WeightData | None:
    """Retrieve weight data for the specified date using Garth API."""
    try:
        login()
        raw = garth.WeightData.get(target_date)
        return raw
    except GarthException as exc:
        log.error("Garth error getting weight data: %s", exc)
        raise

def get_training_readiness_data(target_date: date) -> list[garth.TrainingReadinessData] | None:
    """Retrieve training readiness data for the specified date using Garth API."""
    try:
        login()
        raw = garth.TrainingReadinessData.get(target_date)
        return raw
    except GarthException as exc:
        log.error("Garth error getting training readiness data: %s", exc)
        raise
