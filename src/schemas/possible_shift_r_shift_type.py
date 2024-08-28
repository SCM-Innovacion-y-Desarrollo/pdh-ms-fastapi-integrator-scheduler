from pydantic import BaseModel
from typing import Optional
from datetime import datetime, time

class PossibleShiftRShiftTypeModel(BaseModel):
    possible_shift_r_shift_type_id: Optional[int] = None
    possible_shift_id: int
    shift_type_id: int
    monday: bool = False
    tuesday: bool = False
    wednesday: bool = False
    thursday: bool = False
    friday: bool = False
    saturday: bool = False
    sunday: bool = False
    break_period: int = 1