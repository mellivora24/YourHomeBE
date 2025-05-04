from pydantic import BaseModel
from datetime import datetime

class LogBase(BaseModel):
    content: str
    device_id: int | None = None

class LogCreate(LogBase):
    pass

class Log(LogBase):
    log_id: int
    timestamp: datetime

    class Config:
        from_attributes = True