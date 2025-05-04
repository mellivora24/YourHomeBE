from typing import Callable, Dict
from core.events import DeviceAddedEvent, LogCreatedEvent

class EventBus:
    _subscribers: Dict[str, list[Callable]] = {}

    def subscribe(self, event_type: str, callback: Callable):
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(callback)

    async def publish(self, event):
        event_type = event.__class__.__name__
        if event_type in self._subscribers:
            for callback in self._subscribers[event_type]:
                await callback(event)

event_bus = EventBus()