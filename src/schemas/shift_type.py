from pydantic import BaseModel
from typing import Optional
from datetime import datetime, time

class ShiftTypeModel(BaseModel):
    shift_type_id: Optional[int] = None 
    name: str
    start_time: time
    end_time: time
    duration: time