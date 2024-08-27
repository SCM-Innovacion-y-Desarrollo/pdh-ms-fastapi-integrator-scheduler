from pydantic import BaseModel
from typing import Optional
from datetime import datetime, time

class RuleSetModel(BaseModel):
    ruleset_id: Optional[int] = None
    possible_shift_id: int
    name: str
    description: str
    min_daily_hours: int
    max_daily_hours: int
    min_weekly_hours: int
    max_weekly_hours: int
    min_hours_between_shifts: int
    max_shift_segments_per_shift: int
    night_shift_start_time: time
    night_shift_end_time: time
    min_days_worked_per_week: int
    max_days_worked_per_week: int
    max_consecutive_work_days: int
    max_night_shifts_per_week: int
    max_consecutive_night_shifts: int
    min_days_between_night_shifts: int
    is_active: bool