from pydantic import BaseModel
from typing import Optional
from datetime import datetime, time

class PossibleShiftModel(BaseModel):
    possible_shift_id: Optional[int] = None
    name: str
    description: Optional[str] = None