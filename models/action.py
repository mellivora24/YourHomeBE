from pydantic import BaseModel
from datetime import datetime

class ActionBase(BaseModel):
    command: str
    device_id: int

class ActionCreate(ActionBase):
    pass

class Action(ActionBase):
    action_id: int
    timestamp: datetime

    class Config:
        from_attributes = True