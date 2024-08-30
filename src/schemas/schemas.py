from typing import Generic, List, Optional, TypeVar
from pydantic import BaseModel, ConfigDict

M = TypeVar("M", bound=BaseModel)
T = TypeVar('T', bound=BaseModel)

class ResponseModel(BaseModel, Generic[M]):
    status: Optional[str] = "success"
    data: List[M] | M

class InputModel(BaseModel, Generic[T]):
    data: T
class BaseModelo(BaseModel):

    model_config = ConfigDict(from_attributes=True, str_strip_whitespace=True)

class BaseRequest(BaseModel):
    person_nums: dict[str, int]
    start_date: str
    end_date: str

class ForecastRequest(BaseModel):
    start_date: str
    end_date: str
    path: str