"""Garmin data repository implementing the Repository pattern."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from garth.exc import GarthException
from garth.utils import camel_to_snake_dict

from .client import get_client, ToolError
from .serialization import camel_to_snake_dict as camel_to_snake, project_sleep_fields


class GarminRepository:
    """Repository for Garmin data with data access methods."""

    def __init__(self) -> None:
        """Initialize the repository."""
        self._client = None

    @property
    def client(self) -> garth.http.Client:
        """Get or initialize the Garmin API client."""
        if self._client is None:
            self._client = get_client()
        return self._client

    def weight(self, day: str | None = None) -> dict[str, Any] | None:
        """Get body weight for a day."""
        try:
            from garth.data import WeightData
            result = WeightData.get(day=day, client=self.client)
            return result if result is not None else {}
        except GarthException as e:
            raise ToolError(f"Garmin API error: {str(e)}") from e

    def weight_history(self, end: str | None = None, days: int = 7) -> list[dict[str, Any]] | None:
        """Get weight history for the last N days."""
        try:
            from garth.data import WeightData
            result = WeightData.list(end=end, days=days, client=self.client)
            return [camel_to_snake(entry) for entry in result] if result is not None else []
        except GarthException as e:
            raise ToolError(f"Garmin API error: {str(e)}") from e

    def blood_pressure(self, day: str | None = None) -> dict[str, Any] | None:
        """Get blood pressure for a day."""
        try:
            from garth.data import BloodPressure
            result = BloodPressure.get(day=day, client=self.client)
            return result if result is not None else {}
        except GarthException as e:
            raise ToolError(f"Garmin API error: {str(e)}") from e

    def body_battery(self, day: str | None = None) -> list[dict[str, Any]] | None:
        """Get body battery readings for a day."""
        try:
            from garth.data import BodyBatteryData
            result = BodyBatteryData.get(day=day, client=self.client)
            return [camel_to_snake(entry) for entry in result] if result is not None else []
        except GarthException as e:
            raise ToolError(f"Garmin API error: {str(e)}") from e

    def body_battery_stress(self, day: str | None = None) -> dict[str, Any] | None:
        """Get body battery + stress summary for a day."""
        try:
            from garth.data import DailyBodyBatteryStress
            result = DailyBodyBatteryStress.get(day=day, client=self.client)
            return result if result is not None else {}
        except GarthException as e:
            raise ToolError(f"Garmin API error: {str(e)}") from e

    def body_battery_stress_history(self, end: str | None = None, days: int = 7) -> list[dict[str, Any]] | None:
        """Get body battery + stress history for the last N days."""
        try:
            from garth.data import DailyBodyBatteryStress
            result = DailyBodyBatteryStress.list(end=end, days=days, client=self.client)
            return [camel_to_snake(entry) for entry in result] if result is not None else []
        except GarthException as e:
            raise ToolError(f"Garmin API error: {str(e)}") from e

    def daily_heart_rate(self, day: str | None = None) -> dict[str, Any] | None:
        """Get daily heart rate for a day."""
        try:
            from garth.data import DailyHeartRate
            result = DailyHeartRate.get(day=day, client=self.client)
            return result if result is not None else {}
        except GarthException as e:
            raise ToolError(f"Garmin API error: {str(e)}") from e

    def hrv(self, end: str | None = None, days: int = 28) -> list[dict[str, Any]] | None:
        """Get HRV history for the last N days."""
        try:
            from garth.data.hrv import HRVData
            result = HRVData.list(end=end, period=days, client=self.client)
            return [camel_to_snake(entry) for entry in result] if result is not None else []
        except GarthException as e:
            raise ToolError(f"Garmin API error: {str(e)}") from e

    def resting_heart_rate(self, end: str | None = None, days: int = 1) -> list[dict[str, Any]] | None:
        """Get resting heart rate history for the last N days."""
        try:
            from garth.data import DailyHeartRate
            result = DailyHeartRate.list(end=end, days=days, client=self.client)
            return [camel_to_snake(entry) for entry in result] if result is not None else []
        except GarthException as e:
            raise ToolError(f"Garmin API error: {str(e)}") from e

    def sleep(self, day: str | None = None) -> dict[str, Any] | None:
        """Get sleep data for a day."""
        try:
            import garth
            result = garth.SleepData.get(day=day, client=self.client)
            return result if result is not None else {}
        except GarthException as e:
            raise ToolError(f"Garmin API error: {str(e)}") from e

    def sleep_detail(self, day: str | None = None) -> dict[str, Any] | None:
        """Get sleep details for a day."""
        try:
            from garth.data import DailySleepData
            result = DailySleepData.get(day=day, client=self.client)
            return result if result is not None else {}
        except GarthException as e:
            raise ToolError(f"Garmin API error: {str(e)}") from e

    def sleep_summary(self, day: str | None = None) -> dict[str, Any] | None:
        """Get sleep summary for a day."""
        try:
            from garth.data import DailySummary
            result = DailySummary.get(day=day, client=self.client)
            return project_sleep_fields(result) if result is not None else {}
        except GarthException as e:
            raise ToolError(f"Garmin API error: {str(e)}") from e

    def daily_stress(self, end: str | None = None, days: int = 1) -> list[dict[str, Any]] | None:
        """Get stress history for the last N days."""
        try:
            import garth
            result = garth.DailyStress.list(end=end, period=days, client=self.client)
            return [camel_to_snake(entry) for entry in result] if result is not None else []
        except GarthException as e:
            raise ToolError(f"Garmin API error: {str(e)}") from e

    def weekly_stress(self, end: str | None = None) -> list[dict[str, Any]] | None:
        """Get stress history for the last 7 days."""
        try:
            import garth
            result = garth.DailyStress.list(end=end, period=7, client=self.client)
            return [camel_to_snake(entry) for entry in result] if result is not None else []
        except GarthException as e:
            raise ToolError(f"Garmin API error: {str(e)}") from e

    def training_status_daily(self, day: str | None = None) -> list[dict[str, Any]] | None:
        """Get training status for a day."""
        try:
            from garth.data import TrainingReadinessData
            result = TrainingReadinessData.get(day=day, client=self.client)
            if result is None:
                return []
            return [camel_to_snake(entry) for entry in result]
        except GarthException as e:
            raise ToolError(f"Garmin API error: {str(e)}") from e

    def training_status_weekly(self, end: str | None = None) -> list[dict[str, Any]] | None:
        """Get training status for the last week."""
        try:
            from garth.data import TrainingReadinessData
            result = TrainingReadinessData.get(day=end, client=self.client)
            if result is None:
                return []
            return [camel_to_snake(entry) for entry in result]
        except GarthException as e:
            raise ToolError(f"Garmin API error: {str(e)}") from e

    def training_status_monthly(self, end: str | None = None) -> list[dict[str, Any]] | None:
        """Get training status for the last month."""
        try:
            from garth.data import TrainingReadinessData
            result = TrainingReadinessData.get(day=end, client=self.client)
            if result is None:
                return []
            return [camel_to_snake(entry) for entry in result]
        except GarthException as e:
            raise ToolError(f"Garmin API error: {str(e)}") from e

    def training_readiness(self, day: str | None = None) -> dict[str, Any] | None:
        """Get morning training readiness for a day."""
        try:
            from garth.data import MorningTrainingReadinessData
            result = MorningTrainingReadinessData.get(day=day, client=self.client)
            return result if result is not None else {}
        except GarthException as e:
            raise ToolError(f"Garmin API error: {str(e)}") from e

    def activities(self, limit: int = 20, start: int = 0) -> list[dict[str, Any]] | None:
        """List recent activities."""
        try:
            from garth.data import Activity
            result = Activity.list(limit=limit, start=start, client=self.client)
            return [camel_to_snake(entry) for entry in result] if result is not None else []
        except GarthException as e:
            raise ToolError(f"Garmin API error: {str(e)}") from e

    def activity_detail(self, activity_id: int) -> dict[str, Any] | None:
        """Get details for a single activity."""
        try:
            from garth.data import Activity
            result = Activity.get(activity_id=activity_id, client=self.client)
            return camel_to_snake(result) if result is not None else {}
        except GarthException as e:
            raise ToolError(f"Garmin API error: {str(e)}") from e

    def activity_map(self, activity_id: int) -> dict[str, Any] | None:
        """Get map data (GPS track) for an activity."""
        try:
            from garth.data import Activity
            result = Activity.map_details(activity_id=activity_id, client=self.client)
            return camel_to_snake(result) if result is not None else {}
        except GarthException as e:
            raise ToolError(f"Garmin API error: {str(e)}") from e

    def fitness_activities(self, end: str | None = None, days: int = 7) -> list[dict[str, Any]] | None:
        """Get fitness activities for the last N days."""
        try:
            from garth.data import FitnessActivity
            result = FitnessActivity.list(end=end, days=days, client=self.client)
            return [camel_to_snake(entry) for entry in result] if result is not None else []
        except GarthException as e:
            raise ToolError(f"Garmin API error: {str(e)}") from e

    def personal_records(self) -> list[dict[str, Any]] | None:
        """Get all personal records."""
        try:
            from garth.data import PersonalRecord
            result = PersonalRecord.list(client=self.client)
            return [camel_to_snake(entry) for entry in result] if result is not None else []
        except GarthException as e:
            raise ToolError(f"Garmin API error: {str(e)}") from e

    def personal_record_types(self) -> list[dict[str, Any]] | None:
        """Get available record types."""
        try:
            from garth.data import PersonalRecordType
            result = PersonalRecordType.list(client=self.client)
            return [camel_to_snake(entry) for entry in result] if result is not None else []
        except GarthException as e:
            raise ToolError(f"Garmin API error: {str(e)}") from e

    def daily_steps(self, end: str | None = None) -> list[dict[str, Any]] | None:
        """Get step count for the last day."""
        try:
            import garth
            result = garth.DailySteps.list(end=end, period=1, client=self.client)
            return [camel_to_snake(entry) for entry in result] if result is not None else []
        except GarthException as e:
            raise ToolError(f"Garmin API error: {str(e)}") from e

    def weekly_steps(self, end: str | None = None) -> list[dict[str, Any]] | None:
        """Get step count for the last 7 days."""
        try:
            import garth
            result = garth.DailySteps.list(end=end, period=7, client=self.client)
            return [camel_to_snake(entry) for entry in result] if result is not None else []
        except GarthException as e:
            raise ToolError(f"Garmin API error: {str(e)}") from e

    def daily_summary(self, day: str | None = None) -> dict[str, Any] | None:
        """Get daily summary for a day."""
        try:
            from garth.data import DailySummary
            result = DailySummary.get(day=day, client=self.client)
            return result if result is not None else {}
        except GarthException as e:
            raise ToolError(f"Garmin API error: {str(e)}") from e

    def daily_summary_history(self, end: str | None = None, days: int = 7) -> list[dict[str, Any]] | None:
        """Get daily summary history for the last N days."""
        try:
            from garth.data import DailySummary
            result = DailySummary.list(end=end, days=days, client=self.client)
            return [camel_to_snake(entry) for entry in result] if result is not None else []
        except GarthException as e:
            raise ToolError(f"Garmin API error: {str(e)}") from e

    def daily_hydration(self, day: str | None = None) -> dict[str, Any] | None:
        """Get fluid intake including daily goal for a day."""
        try:
            import garth
            result = garth.DailyHydration.all_data(day=day, client=self.client)
            return result if result is not None else {}
        except GarthException as e:
            raise ToolError(f"Garmin API error: {str(e)}") from e

    def hydration_history(self, end: str | None = None, days: int = 1) -> list[dict[str, Any]] | None:
        """Get fluid intake history for the last N days."""
        try:
            import garth
            result = garth.DailyHydration.list(end=end, period=days, client=self.client)
            return [camel_to_snake(entry) for entry in result] if result is not None else []
        except GarthException as e:
            raise ToolError(f"Garmin API error: {str(e)}") from e

    def device_info(self) -> dict[str, Any] | None:
        """Get active Garmin device info."""
        try:
            import garth
            # Try the deviceinfo endpoint; fall back to user profile
            try:
                raw = self.client.connectapi(
                    '/connectapi/proxy/deviceinfo-service/device', method='GET'
                )
                return camel_to_snake(raw) if raw else {}
            except Exception:
                # Fallback: extract from user profile
                profile = garth.UserProfile.get(client=self.client)
                result = profile
                device_keys = {k: v for k, v in result.items() if 'device' in k.lower()}
                return device_keys if device_keys else result
        except GarthException as e:
            raise ToolError(f"Garmin API error: {str(e)}") from e

    def connected_devices(self) -> list[dict[str, Any]] | None:
        """Get list of all connected Garmin devices."""
        try:
            import garth
            try:
                raw = self.client.connectapi(
                    '/connectapi/proxy/deviceinfo-service/devices', method='GET'
                )
                if isinstance(raw, list):
                    return [camel_to_snake(d) for d in raw]
                if isinstance(raw, dict):
                    return [camel_to_snake(raw)]
                return []
            except Exception:
                # Fallback: try user profile
                try:
                    profile = garth.UserProfile.get(client=self.client)
                    result = profile
                    devices = result.get('devices', result.get('connected_devices', []))
                    if isinstance(devices, list):
                        return devices
                    return []
                except Exception:
                    return []
        except GarthException as e:
            raise ToolError(f"Garmin API error: {str(e)}") from e

    def nutrition_log(self, day: str | None = None) -> dict[str, Any] | None:
        """Get nutrition log for a day."""
        try:
            from garth.data import NutritionLog
            result = NutritionLog.get(day=day, client=self.client)
            return result if result is not None else {}
        except GarthException as e:
            raise ToolError(f"Garmin API error: {str(e)}") from e

    def nutrition_status(self) -> dict[str, Any] | None:
        """Get nutrition status."""
        try:
            from garth.data import NutritionStatus
            result = NutritionStatus.get(client=self.client)
            return result if result is not None else {}
        except GarthException as e:
            raise ToolError(f"Garmin API error: {str(e)}") from e

    def steps_goal(self, day: str | None = None) -> dict[str, Any] | None:
        """Get steps goal for a day."""
        try:
            from garth.data import StepsGoal
            result = StepsGoal.get(day=day, client=self.client)
            return result if result is not None else {}
        except GarthException as e:
            raise ToolError(f"Garmin API error: {str(e)}") from e

    def weight_goal(self, day: str | None = None) -> dict[str, Any] | None:
        """Get weight goal for a day."""
        try:
            from garth.data import WeightGoal
            result = WeightGoal.get(day=day, client=self.client)
            return result if result is not None else {}
        except GarthException as e:
            raise ToolError(f"Garmin API error: {str(e)}") from e

    def garmin_scores(self, day: str | None = None) -> dict[str, Any] | None:
        """Get Garmin fitness scores for a day."""
        try:
            import garth
            result = garth.GarminScoresData.get(day=day, client=self.client)
            return result if result is not None else {}
        except GarthException as e:
            raise ToolError(f"Garmin API error: {str(e)}") from e

    def user_profile(self) -> dict[str, Any] | None:
        """Get Garmin user profile."""
        try:
            import garth
            result = garth.UserProfile.get(client=self.client)
            return result if result is not None else {}
        except GarthException as e:
            raise ToolError(f"Garmin API error: {str(e)}") from e

    def user_settings(self) -> dict[str, Any] | None:
        """Get user settings."""
        try:
            import garth
            result = garth.UserSettings.get(client=self.client)
            return result if result is not None else {}
        except GarthException as e:
            raise ToolError(f"Garmin API error: {str(e)}") from e