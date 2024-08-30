from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from enum import Enum

class ForecastModel(BaseModel):
    model_config = ConfigDict(from_attributes=True) 
    forecast_id: Optional[int] = None
    date: datetime
    value: float
    path: str