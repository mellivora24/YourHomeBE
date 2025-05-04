from abc import ABC, abstractmethod
from typing import List

class IMQTTService(ABC):
    @abstractmethod
    async def get_available_ports(self, home_id: int) -> List[int]:
        pass

    @abstractmethod
    async def send_command(self, device_id: int, command: str):
        pass