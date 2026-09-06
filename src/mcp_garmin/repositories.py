"""GarminRepository - Data source abstraction for Garmin API endpoints."""

from __future__ import annotations

from typing import Any

import garth
from garth.exc import GarthException
from garth.utils import asdict

from .errors import ToolError


class GarminRepository:
    """Repository pattern for Garmin data endpoints."""

    def __init__(self, client: garth.http.Client | None = None):
        """Initialize repository with optional client."""
        self._client = client

    def _get_client(self) -> garth.http.Client:
        """Get or create the garth client."""
        if self._client is not None:
            return self._client
        # Import here to avoid circular imports
        from .client import get_client
        self._client = get_client()
        return self._client

    def _from_garmin(self, func, *args, **kwargs) -> Any:
        """Wrap garth calls with error handling."""
        try:
            return func(*args, **kwargs)
        except GarthException as e:
            raise ToolError(str(e)) from e

    def weight(self, day: str | None = None) -> dict:
        """Body weight for a day (YYYY-MM-DD) — grams, BMI, body fat, etc."""
        client = self._get_client()
        from garth.data import WeightData
        
        result = self._from_garmin(WeightData.get, day=day, client=client)
        return asdict(result) if result is not None else {}

    def weight_history(self, end: str | None = None, days: int = 7) -> list[dict]:
        """Weight history for the last N days (up to end, YYYY-MM-DD)."""
        client = self._get_client()
        from garth.data import WeightData
        
        result = self._from_garmin(WeightData.list, end=end, days=days, client=client)
        return [asdict(entry) for entry in result]

    def blood_pressure(self, day: str | None = None) -> dict:
        """Blood pressure reading for a day (YYYY-MM-DD)."""
        client = self._get_client()
        from garth.data import BloodPressure
        
        result = self._from_garmin(BloodPressure.get, day=day, client=client)
        return asdict(result) if result is not None else {}

    def body_battery(self, day: str | None = None) -> list[dict]:
        """Body Battery readings for a day (YYYY-MM-DD)."""
        client = self._get_client()
        from garth.data import BodyBatteryData
        
        result = self._from_garmin(BodyBatteryData.get, day=day, client=client)
        return [asdict(entry) for entry in result]

    def body_battery_stress(self, day: str | None = None) -> dict:
        """Body Battery + stress summary for a day (YYYY-MM-DD)."""
        client = self._get_client()
        from garth.data import DailyBodyBatteryStress
        
        result = self._from_garmin(DailyBodyBatteryStress.get, day=day, client=client)
        return asdict(result) if result is not None else {}

    def body_battery_stress_history(self, end: str | None = None, days: int = 7) -> list[dict]:
        """Body Battery + stress history for the last N days (up to end)."""
        client = self._get_client()
        from garth.data import DailyBodyBatteryStress
        
        result = self._from_garmin(DailyBodyBatteryStress.list, end=end, days=days, client=client)
        return [asdict(entry) for entry in result]

    def daily_heart_rate(self, day: str | None = None) -> dict:
        """Daily heart rate for a day (YYYY-MM-DD)."""
        client = self._get_client()
        from garth.data import DailyHeartRate
        
        result = self._from_garmin(DailyHeartRate.get, day=day, client=client)
        return asdict(result) if result is not None else {}

    def hrv(self, end: str | None = None, period: int = 7) -> list[dict]:
        """HRV data for the last N days (up to end)."""
        client = self._get_client()
        from garth.data import HRVData
        
        result = self._from_garmin(HRVData.list, end=end, period=period, client=client)
        return [asdict(entry) for entry in result]

    def resting_heart_rate(self, end: str | None = None, days: int = 7) -> list[dict]:
        """Resting heart rate for the last N days (up to end)."""
        client = self._get_client()
        from garth.data import DailyHeartRate
        
        result = self._from_garmin(DailyHeartRate.list, end=end, days=days, client=client)
        return [asdict(entry) for entry in result]

    def sleep(self, day: str | None = None) -> dict:
        """Sleep data for a day (YYYY-MM-DD) including sleep stage time blocks."""
        client = self._get_client()
        import garth
        
        result = self._from_garmin(garth.SleepData.get, day=day, client=client)
        return asdict(result) if result is not None else {}

    def sleep_detail(self, day: str | None = None) -> dict:
        """Sleep details (daily data) for a day (YYYY-MM-DD)."""
        client = self._get_client()
        from garth.data import DailySleepData
        
        result = self._from_garmin(DailySleepData.get, day=day, client=client)
        return asdict(result) if result is not None else {}

    def sleep_summary(self, day: str | None = None) -> dict:
        """Daily summary for a day (YYYY-MM-DD)."""
        client = self._get_client()
        from garth.data import DailySummary
        
        result = self._from_garmin(DailySummary.get, day=day, client=client)
        return asdict(result) if result is not None else {}

    def daily_stress(self, end: str | None = None, period: int = 7) -> list[dict]:
        """Daily stress data for the last N days (up to end)."""
        client = self._get_client()
        from garth.data import DailyStress
        
        result = self._from_garmin(DailyStress.list, end=end, period=period, client=client)
        return [asdict(entry) for entry in result]

    def weekly_stress(self, end: str | None = None, period: int = 7) -> list[dict]:
        """Weekly stress data for the last N weeks (up to end)."""
        client = self._get_client()
        from garth.data import DailyStress
        
        result = self._from_garmin(DailyStress.list, end=end, period=period, client=client)
        return [asdict(entry) for entry in result]

    def training_status_daily(self, day: str | None = None) -> dict:
        """Training status for a day (YYYY-MM-DD)."""
        client = self._get_client()
        from garth.data import TrainingReadinessData
        
        result = self._from_garmin(TrainingReadinessData.get, day=day, client=client)
        return asdict(result) if result is not None else {}

    def training_status_weekly(self, end: str | None = None, period: int = 7) -> list[dict]:
        """Training status for the last N weeks (up to end)."""
        client = self._get_client()
        from garth.data import TrainingReadinessData
        
        result = self._from_garmin(TrainingReadinessData.list, end=end, period=period, client=client)
        return [asdict(entry) for entry in result]

    def training_status_monthly(self, end: str | None = None, period: int = 7) -> list[dict]:
        """Training status for the last N months (up to end)."""
        client = self._get_client()
        from garth.data import TrainingReadinessData
        
        result = self._from_garmin(TrainingReadinessData.list, end=end, period=period, client=client)
        return [asdict(entry) for entry in result]

    def training_readiness(self, day: str | None = None) -> dict:
        """Training readiness for a day (YYYY-MM-DD)."""
        client = self._get_client()
        from garth.data import TrainingReadinessData
        
        result = self._from_garmin(TrainingReadinessData.get, day=day, client=client)
        return asdict(result) if result is not None else {}

    def morning_training_readiness(self, day: str | None = None) -> dict:
        """Morning training readiness for a day (YYYY-MM-DD)."""
        client = self._get_client()
        from garth.data import MorningTrainingReadinessData
        
        result = self._from_garmin(MorningTrainingReadinessData.get, day=day, client=client)
        return asdict(result) if result is not None else {}

    def activities(self, limit: int = 20, start: int = 0) -> list[dict]:
        """List of recent activities (limit/start pagination)."""
        client = self._get_client()
        from garth.data import Activity
        
        result = self._from_garmin(Activity.list, limit=limit, start=start, client=client)
        return [asdict(entry) for entry in result]

    def activity_detail(self, activity_id: int) -> dict:
        """Details for a single activity (activity_id)."""
        client = self._get_client()
        from garth.data import Activity
        
        result = self._from_garmin(Activity.get, activity_id=activity_id, client=client)
        return asdict(result) if result is not None else {}

    def activity_map(self, activity_id: int) -> dict:
        """Map data (GPS track) for an activity (activity_id)."""
        client = self._get_client()
        from garth.data import Activity
        
        result = self._from_garmin(Activity.map_details, activity_id=activity_id, client=client)
        return asdict(result) if result is not None else {}

    def fitness_activities(self, end: str | None = None, days: int = 7) -> list[dict]:
        """Fitness activities (steps/calories) for the last N days (up to end)."""
        client = self._get_client()
        from garth.data import FitnessActivity
        
        result = self._from_garmin(FitnessActivity.list, end=end, days=days, client=client)
        return [asdict(entry) for entry in result]

    def personal_records(self) -> list[dict]:
        """All personal records."""
        client = self._get_client()
        from garth.data import PersonalRecord
        
        result = self._from_garmin(PersonalRecord.list, client=client)
        return [asdict(entry) for entry in result]

    def personal_record_types(self) -> list[dict]:
        """Available record types."""
        client = self._get_client()
        from garth.data import PersonalRecordType
        
        result = self._from_garmin(PersonalRecordType.list, client=client)
        return [asdict(entry) for entry in result]

    def daily_steps(self, end: str | None = None, period: int = 1) -> list[dict]:
        """Daily steps for the last N days (up to end)."""
        client = self._get_client()
        from garth.data import DailySteps
        
        result = self._from_garmin(DailySteps.list, end=end, period=period, client=client)
        return [asdict(entry) for entry in result]

    def weekly_steps(self, end: str | None = None, period: int = 7) -> list[dict]:
        """Weekly steps for the last N weeks (up to end)."""
        client = self._get_client()
        from garth.data import DailySteps
        
        result = self._from_garmin(DailySteps.list, end=end, period=period, client=client)
        return [asdict(entry) for entry in result]

    def daily_summary(self, day: str | None = None) -> dict:
        """Daily summary for a day (YYYY-MM-DD)."""
        client = self._get_client()
        from garth.data import DailySummary
        
        result = self._from_garmin(DailySummary.get, day=day, client=client)
        return asdict(result) if result is not None else {}

    def daily_summary_history(self, end: str | None = None, days: int = 7) -> list[dict]:
        """Daily summary history for the last N days (up to end)."""
        client = self._get_client()
        from garth.data import DailySummary
        
        result = self._from_garmin(DailySummary.list, end=end, days=days, client=client)
        return [asdict(entry) for entry in result]

    def daily_hydration(self, end: str | None = None, period: int = 1) -> list[dict]:
        """Daily hydration for the last N days (up to end)."""
        client = self._get_client()
        from garth.data import DailyHydration
        
        result = self._from_garmin(DailyHydration.list, end=end, period=period, client=client)
        return [asdict(entry) for entry in result]

    def hydration_history(self, end: str | None = None, days: int = 7) -> list[dict]:
        """Hydration history for the last N days (up to end)."""
        client = self._get_client()
        from garth.data import DailyHydration
        
        result = self._from_garmin(DailyHydration.list, end=end, days=days, client=client)
        return [asdict(entry) for entry in result]

    def device_info(self) -> dict:
        """Active Garmin device: type, name, battery level."""
        client = self._get_client()
        from garth.utils import camel_to_snake_dict
        
        # Try the deviceinfo endpoint; fall back to user profile
        try:
            raw = client.connectapi(
                '/connectapi/proxy/deviceinfo-service/device', method='GET'
            )
            return camel_to_snake_dict(raw) if raw else {}
        except Exception:
            # Fallback: extract from user profile
            from garth.data import UserProfile
            profile = self._from_garmin(UserProfile.get, client=client)
            result = asdict(profile)
            device_keys = {k: v for k, v in result.items() if 'device' in k.lower()}
            return device_keys if device_keys else result

    def connected_devices(self) -> list[dict]:
        """List of all connected Garmin devices."""
        client = self._get_client()
        from garth.utils import camel_to_snake_dict
        
        try:
            raw = client.connectapi(
                '/connectapi/proxy/deviceinfo-service/devices', method='GET'
            )
            if isinstance(raw, list):
                return [camel_to_snake_dict(d) for d in raw]
            if isinstance(raw, dict):
                return [camel_to_snake_dict(raw)]
            return []
        except Exception:
            # Fallback: try user profile
            try:
                from garth.data import UserProfile
                profile = self._from_garmin(UserProfile.get, client=client)
                result = asdict(profile)
                devices = result.get('devices', result.get('connected_devices', []))
                if isinstance(devices, list):
                    return devices
                return []
            except Exception:
                return []

    def nutrition_log(self, day: str | None = None) -> dict:
        """Nutrition log for a day (YYYY-MM-DD)."""
        client = self._get_client()
        from garth.data import NutritionLog
        
        result = self._from_garmin(NutritionLog.get, day=day, client=client)
        return asdict(result) if result is not None else {}

    def nutrition_status(self) -> dict:
        """Nutrition status."""
        client = self._get_client()
        from garth.data import NutritionStatus
        
        result = self._from_garmin(NutritionStatus.get, client=client)
        return asdict(result) if result is not None else {}

    def steps_goal(self, day: str | None = None) -> dict:
        """Steps goal for a day (YYYY-MM-DD) — device + user + sync status."""
        client = self._get_client()
        from garth.data import StepsGoal
        
        result = self._from_garmin(StepsGoal.get, day=day, client=client)
        return asdict(result) if result is not None else {}

    def weight_goal(self, day: str | None = None) -> dict:
        """Weight goal for a day (YYYY-MM-DD) — target + target ranges."""
        client = self._get_client()
        from garth.data import WeightGoal
        
        result = self._from_garmin(WeightGoal.get, day=day, client=client)
        return asdict(result) if result is not None else {}

    def garmin_scores(self, day: str | None = None) -> dict:
        """Garmin fitness scores for a day (YYYY-MM-DD) — Vo2Max, Endurance, Power."""
        client = self._get_client()
        import garth
        
        result = self._from_garmin(garth.GarminScoresData.get, day=day, client=client)
        return asdict(result) if result is not None else {}

    def user_profile(self) -> dict:
        """User profile data."""
        client = self._get_client()
        from garth.data import UserProfile
        
        result = self._from_garmin(UserProfile.get, client=client)
        return asdict(result) if result is not None else {}

    def user_settings(self) -> dict:
        """User settings data."""
        client = self._get_client()
        from garth.data import UserSettings
        
        result = self._from_garmin(UserSettings.get, client=client)
        return asdict(result) if result is not None else {}