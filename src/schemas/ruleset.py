from pydantic import BaseModel
from typing import Optional
from datetime import datetime, time

class RuleSetModel(BaseModel):
    ruleset_id: Optional[int] = None
    possible_shift_id: int
    name: str
    description: str
    min_daily_hours: float
    max_daily_hours: float
    min_weekly_hours: float
    max_weekly_hours: float
    min_hours_between_shifts: float
    max_shift_segments_per_shift: int
    night_shift_start_time: time
    night_shift_end_time: time
    min_days_worked_per_week: int
    max_days_worked_per_week: int
    max_consecutive_work_days: int
    max_night_shifts_per_week: int
    max_consecutive_night_shifts: Optional[int] = None
    min_days_between_night_shifts:  Optional[int] = None
    is_active: bool