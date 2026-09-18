from __future__ import annotations

import asyncio
from collections import deque
from copy import deepcopy

from .models import Event, JarvisState, Presence


class StateStore:
    def __init__(self) -> None:
        self.state = JarvisState(
            devices=[
                {
                    "id": "CSI-001",
                    "name": "Living Room Sensor",
                    "zone": "living-room",
                    "status": "online",
                    "signal_strength": 0.91,
                },
                {
                    "id": "CSI-002",
                    "name": "Hallway Sensor",
                    "zone": "hallway",
                    "status": "online",
                    "signal_strength": 0.78,
                },
            ]
        )
        self.events: deque[Event] = deque(maxlen=100)
        self.sequence = 0
        self.subscribers: set[asyncio.Queue[Event]] = set()

    def snapshot(self) -> JarvisState:
        return deepcopy(self.state)

    def update_presence(self, count: int, confidence: float) -> None:
        self.state.presence = Presence(count=count, confidence=confidence)

    def update_activity(self, activity) -> None:
        self.state.activity = activity

    def update_signal(self, **values) -> None:
        self.state.signal = self.state.signal.model_copy(update=values)

    async def publish(self, event: Event) -> None:
        self.sequence += 1
        event.sequence = self.sequence
        self.events.append(event)
        self.state.last_event = event
        for queue in list(self.subscribers):
            if queue.full():
                try:
                    queue.get_nowait()
                except asyncio.QueueEmpty:
                    pass
            await queue.put(event)

    def subscribe(self) -> asyncio.Queue[Event]:
        queue: asyncio.Queue[Event] = asyncio.Queue(maxsize=50)
        self.subscribers.add(queue)
        return queue

    def unsubscribe(self, queue: asyncio.Queue[Event]) -> None:
        self.subscribers.discard(queue)
