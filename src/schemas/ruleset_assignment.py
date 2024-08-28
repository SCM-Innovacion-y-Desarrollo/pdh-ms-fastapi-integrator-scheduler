from pydantic import BaseModel
from typing import Optional
from datetime import datetime, time

class RulesetAssignmentModel(BaseModel):
    ruleset_assignment_id: Optional[int] = None
    employee_id: int
    ruleset_id: int
    start_date: datetime
    end_date: datetime
    last_modified: datetime


    