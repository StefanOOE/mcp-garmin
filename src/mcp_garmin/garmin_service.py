"""Garmin service facade implementing business logic."""

from __future__ import annotations

from typing import Any

from .errors import ToolError
from .repositories import GarminRepository
from .serialization import project_sleep_fields


class GarminService:
    """Facade for Garmin data with business logic."""

    def __init__(self, repository: GarminRepository) -> None:
        """Initialize the service with a repository."""
        self.repository = repository

    def weight(self, day: str | None = None) -> dict[str, Any]:
        """Get body weight for a day."""
        try:
            result = self.repository.weight(day=day)
            return result if result is not None else {}
        except ToolError:
            raise
        except Exception:
            # Handle any unexpected errors gracefully
            return {}

    def weight_history(self, end: str | None = None, days: int = 7) -> list[dict[str, Any]]:
        """Get weight history for the last N days."""
        try:
            result = self.repository.weight_history(end=end, days=days)
            return result if result is not None else []
        except ToolError:
            raise
        except Exception:
            # Handle any unexpected errors gracefully
            return []

    def blood_pressure(self, day: str | None = None) -> dict[str, Any]:
        """Get blood pressure for a day."""
        try:
            result = self.repository.blood_pressure(day=day)
            return result if result is not None else {}
        except ToolError:
            raise
        except Exception:
            # Handle any unexpected errors gracefully
            return {}

    def body_battery(self, day: str | None = None) -> list[dict[str, Any]]:
        """Get body battery readings for a day."""
        try:
            result = self.repository.body_battery(day=day)
            return result if result is not None else []
        except ToolError:
            raise
        except Exception:
            # Handle any unexpected errors gracefully
            return []

    def body_battery_stress(self, day: str | None = None) -> dict[str, Any]:
        """Get body battery + stress summary for a day."""
        try:
            result = self.repository.body_battery_stress(day=day)
            return result if result is not None else {}
        except ToolError:
            raise
        except Exception:
            # Handle any unexpected errors gracefully
            return {}

    def body_battery_stress_history(self, end: str | None = None, days: int = 7) -> list[dict[str, Any]]:
        """Get body battery + stress history for the last N days."""
        try:
            result = self.repository.body_battery_stress_history(end=end, days=days)
            return result if result is not None else []
        except ToolError:
            raise
        except Exception:
            # Handle any unexpected errors gracefully
            return []

    def daily_heart_rate(self, day: str | None = None) -> dict[str, Any]:
        """Get daily heart rate for a day."""
        try:
            result = self.repository.daily_heart_rate(day=day)
            return result if result is not None else {}
        except ToolError:
            raise
        except Exception:
            # Handle any unexpected errors gracefully
            return {}

    def hrv(self, end: str | None = None, days: int = 28) -> list[dict[str, Any]]:
        """Get HRV history for the last N days."""
        try:
            result = self.repository.hrv(end=end, days=days)
            return result if result is not None else []
        except ToolError:
            raise
        except Exception:
            # Handle any unexpected errors gracefully
            return []

    def resting_heart_rate(self, end: str | None = None, days: int = 1) -> list[dict[str, Any]]:
        """Get resting heart rate history for the last N days."""
        try:
            result = self.repository.resting_heart_rate(end=end, days=days)
            return result if result is not None else []
        except ToolError:
            raise
        except Exception:
            # Handle any unexpected errors gracefully
            return []

    def sleep(self, day: str | None = None) -> dict[str, Any]:
        """Get sleep data for a day."""
        try:
            result = self.repository.sleep(day=day)
            return result if result is not None else {}
        except ToolError:
            raise
        except Exception:
            # Handle any unexpected errors gracefully
            return {}

    def sleep_detail(self, day: str | None = None) -> dict[str, Any]:
        """Get sleep details for a day."""
        try:
            result = self.repository.sleep_detail(day=day)
            return result if result is not None else {}
        except ToolError:
            raise
        except Exception:
            # Handle any unexpected errors gracefully
            return {}

    def sleep_summary(self, day: str | None = None) -> dict[str, Any]:
        """Get sleep summary for a day."""
        try:
            result = self.repository.sleep_summary(day=day)
            return project_sleep_fields(result)
        except ToolError:
            raise
        except Exception:
            # Handle any unexpected errors gracefully
            return {}

    def daily_stress(self, end: str | None = None, days: int = 1) -> list[dict[str, Any]]:
        """Get stress history for the last N days."""
        try:
            result = self.repository.daily_stress(end=end, days=days)
            return result if result is not None else []
        except ToolError:
            raise
        except Exception:
            # Handle any unexpected errors gracefully
            return []

    def weekly_stress(self, end: str | None = None) -> list[dict[str, Any]]:
        """Get stress history for the last 7 days."""
        try:
            result = self.repository.weekly_stress(end=end)
            return result if result is not None else []
        except ToolError:
            raise
        except Exception:
            # Handle any unexpected errors gracefully
            return []

    def training_status_daily(self, day: str | None = None) -> list[dict[str, Any]]:
        """Get training status for a day."""
        try:
            result = self.repository.training_status_daily(day=day)
            return result if result is not None else []
        except ToolError:
            raise
        except Exception:
            # Handle any unexpected errors gracefully
            return []

    def training_status_weekly(self, end: str | None = None) -> list[dict[str, Any]]:
        """Get training status for the last week."""
        try:
            result = self.repository.training_status_weekly(end=end)
            return result if result is not None else []
        except ToolError:
            raise
        except Exception:
            # Handle any unexpected errors gracefully
            return []

    def training_status_monthly(self, end: str | None = None) -> list[dict[str, Any]]:
        """Get training status for the last month."""
        try:
            result = self.repository.training_status_monthly(end=end)
            return result if result is not None else []
        except ToolError:
            raise
        except Exception:
            # Handle any unexpected errors gracefully
            return []

    def training_readiness(self, day: str | None = None) -> dict[str, Any]:
        """Get morning training readiness for a day."""
        try:
            result = self.repository.training_readiness(day=day)
            return result if result is not None else {}
        except ToolError:
            raise
        except Exception:
            # Handle any unexpected errors gracefully
            return {}

    def morning_readiness(self, day: str | None = None) -> dict[str, Any]:
        """Get morning readiness for a day."""
        return self.training_readiness(day=day)

    def activities(self, limit: int = 20, start: int = 0) -> list[dict[str, Any]]:
        """List recent activities."""
        try:
            result = self.repository.activities(limit=limit, start=start)
            return result if result is not None else []
        except ToolError:
            raise
        except Exception:
            # Handle any unexpected errors gracefully
            return []

    def activity_detail(self, activity_id: int) -> dict[str, Any]:
        """Get details for a single activity."""
        try:
            result = self.repository.activity_detail(activity_id=activity_id)
            return result if result is not None else {}
        except ToolError:
            raise
        except Exception:
            # Handle any unexpected errors gracefully
            return {}

    def activity_map(self, activity_id: int) -> dict[str, Any]:
        """Get map data (GPS track) for an activity."""
        try:
            result = self.repository.activity_map(activity_id=activity_id)
            return result if result is not None else {}
        except ToolError:
            raise
        except Exception:
            # Handle any unexpected errors gracefully
            return {}

    def fitness_activities(self, end: str | None = None, days: int = 7) -> list[dict[str, Any]]:
        """Get fitness activities for the last N days."""
        try:
            result = self.repository.fitness_activities(end=end, days=days)
            return result if result is not None else []
        except ToolError:
            raise
        except Exception:
            # Handle any unexpected errors gracefully
            return []

    def personal_records(self) -> list[dict[str, Any]]:
        """Get all personal records."""
        try:
            result = self.repository.personal_records()
            return result if result is not None else []
        except ToolError:
            raise
        except Exception:
            # Handle any unexpected errors gracefully
            return []

    def personal_record_types(self) -> list[dict[str, Any]]:
        """Get available record types."""
        try:
            result = self.repository.personal_record_types()
            return result if result is not None else []
        except ToolError:
            raise
        except Exception:
            # Handle any unexpected errors gracefully
            return []

    def daily_steps(self, end: str | None = None) -> list[dict[str, Any]]:
        """Get step count for the last day."""
        try:
            result = self.repository.daily_steps(end=end)
            return result if result is not None else []
        except ToolError:
            raise
        except Exception:
            # Handle any unexpected errors gracefully
            return []

    def weekly_steps(self, end: str | None = None) -> list[dict[str, Any]]:
        """Get step count for the last 7 days."""
        try:
            result = self.repository.weekly_steps(end=end)
            return result if result is not None else []
        except ToolError:
            raise
        except Exception:
            # Handle any unexpected errors gracefully
            return []

    def daily_summary(self, day: str | None = None) -> dict[str, Any]:
        """Get daily summary for a day."""
        try:
            result = self.repository.daily_summary(day=day)
            return result if result is not None else {}
        except ToolError:
            raise
        except Exception:
            # Handle any unexpected errors gracefully
            return {}

    def daily_summary_history(self, end: str | None = None, days: int = 7) -> list[dict[str, Any]]:
        """Get daily summary history for the last N days."""
        try:
            result = self.repository.daily_summary_history(end=end, days=days)
            return result if result is not None else []
        except ToolError:
            raise
        except Exception:
            # Handle any unexpected errors gracefully
            return []

    def daily_hydration(self, day: str | None = None) -> dict[str, Any]:
        """Get fluid intake including daily goal for a day."""
        try:
            result = self.repository.daily_hydration(day=day)
            return result if result is not None else {}
        except ToolError:
            raise
        except Exception:
            # Handle any unexpected errors gracefully
            return {}

    def hydration_history(self, end: str | None = None, days: int = 1) -> list[dict[str, Any]]:
        """Get fluid intake history for the last N days."""
        try:
            result = self.repository.hydration_history(end=end, days=days)
            return result if result is not None else []
        except ToolError:
            raise
        except Exception:
            # Handle any unexpected errors gracefully
            return []

    def device_info(self) -> dict[str, Any]:
        """Get active Garmin device info."""
        try:
            result = self.repository.device_info()
            return result if result is not None else {}
        except ToolError:
            raise
        except Exception:
            # Handle any unexpected errors gracefully
            return {}

    def connected_devices(self) -> list[dict[str, Any]]:
        """Get list of all connected Garmin devices."""
        try:
            result = self.repository.connected_devices()
            return result if result is not None else []
        except ToolError:
            raise
        except Exception:
            # Handle any unexpected errors gracefully
            return []

    def nutrition_log(self, day: str | None = None) -> dict[str, Any]:
        """Get nutrition log for a day."""
        try:
            result = self.repository.nutrition_log(day=day)
            return result if result is not None else {}
        except ToolError:
            raise
        except Exception:
            # Handle any unexpected errors gracefully
            return {}

    def nutrition_status(self) -> dict[str, Any]:
        """Get nutrition status."""
        try:
            result = self.repository.nutrition_status()
            return result if result is not None else {}
        except ToolError:
            raise
        except Exception:
            # Handle any unexpected errors gracefully
            return {}

    def steps_goal(self, day: str | None = None) -> dict[str, Any]:
        """Get steps goal for a day."""
        try:
            result = self.repository.steps_goal(day=day)
            return result if result is not None else {}
        except ToolError:
            raise
        except Exception:
            # Handle any unexpected errors gracefully
            return {}

    def weight_goal(self, day: str | None = None) -> dict[str, Any]:
        """Get weight goal for a day."""
        try:
            result = self.repository.weight_goal(day=day)
            return result if result is not None else {}
        except ToolError:
            raise
        except Exception:
            # Handle any unexpected errors gracefully
            return {}

    def garmin_scores(self, day: str | None = None) -> dict[str, Any]:
        """Get Garmin fitness scores for a day."""
        try:
            result = self.repository.garmin_scores(day=day)
            return result if result is not None else {}
        except ToolError:
            raise
        except Exception:
            # Handle any unexpected errors gracefully
            return {}

    def user_profile(self) -> dict[str, Any]:
        """Get Garmin user profile."""
        try:
            result = self.repository.user_profile()
            return result if result is not None else {}
        except ToolError:
            raise
        except Exception:
            # Handle any unexpected errors gracefully
            return {}

    def user_settings(self) -> dict[str, Any]:
        """Get user settings."""
        try:
            result = self.repository.user_settings()
            return result if result is not None else {}
        except ToolError:
            raise
        except Exception:
            # Handle any unexpected errors gracefully
            return {}