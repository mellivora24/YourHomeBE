from pydantic import BaseModel

class SensorBase(BaseModel):
    port: int
    type: str
    has: bool
    device_id: int

class SensorCreate(BaseModel):
    room_id: int
    device_id: int
    name: str
    type: str = "unknown"
    value: float = 0.0

class Sensor(SensorBase):
    sensor_id: int

    class Config:
        from_attributes = True