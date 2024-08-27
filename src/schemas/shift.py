from pydantic import BaseModel
from typing import Optional
from datetime import datetime, time

class ShiftModel(BaseModel):
    shift_id: Optional[int] = None
    employee_id: int
    date: datetime
    start_ts: time
    end_ts: time
    duration: time
    timezone: str
    override: bool
    scheduler_create: bool
    enable: bool