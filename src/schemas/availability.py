from pydantic import BaseModel
from typing import Optional
from datetime import date

class AvailabilityModel(BaseModel):
    availability_id : Optional[int] = None
    employee_id: int
    date: date
    data: str