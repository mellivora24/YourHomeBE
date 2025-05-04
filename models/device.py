from pydantic import BaseModel
from datetime import datetime

class DeviceBase(BaseModel):
    name: str
    port: int
    status: bool = False
    value: int
    room_id: int
    home_id: int

class DeviceCreate(DeviceBase):
    pass

class Device(DeviceBase):
    device_id: int
    created_at: datetime

    class Config:
        from_attributes = True