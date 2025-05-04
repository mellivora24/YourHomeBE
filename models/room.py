from pydantic import BaseModel

class RoomBase(BaseModel):
    name: str
    home_id: int

class RoomCreate(RoomBase):
    pass

class Room(RoomBase):
    room_id: int

    class Config:
        from_attributes = True