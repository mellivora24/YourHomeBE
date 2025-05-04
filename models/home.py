from pydantic import BaseModel
from datetime import datetime

class HomeBase(BaseModel):
    name: str
    user_id: int

class HomeCreate(HomeBase):
    pass

class Home(HomeBase):
    home_id: int
    created_at: datetime
    last_online: datetime | None = None

    class Config:
        from_attributes = True