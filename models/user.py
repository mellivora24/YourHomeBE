from pydantic import BaseModel
from datetime import datetime

class UserBase(BaseModel):
    name: str
    avatar: str | None = None
    phone: str | None = None
    email: str
    password: str
    role: str = "user"

class UserCreate(UserBase):
    pass

class User(UserBase):
    user_id: int
    auth_id: str | None = None
    created_at: datetime

    class Config:
        from_attributes = True