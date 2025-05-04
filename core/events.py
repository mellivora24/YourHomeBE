from dataclasses import dataclass

@dataclass
class DeviceAddedEvent:
    device_id: int
    home_id: int

@dataclass
class LogCreatedEvent:
    log_id: int
    device_id: int
    content: str