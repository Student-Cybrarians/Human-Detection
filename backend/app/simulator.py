from __future__ import annotations

import asyncio
import math
from contextlib import suppress

from .models import Activity, Event
from .store import StateStore


class DetectionSimulator:
    """Deterministic signal simulator used until a real CSI adapter is attached."""

    def __init__(self, store: StateStore) -> None:
        self.store = store
        self.tick = 0
        self.task: asyncio.Task | None = None

    async def start(self) -> None:
        if self.task and not self.task.done():
            return
        self.task = asyncio.create_task(self._run())

    async def stop(self) -> None:
        if not self.task:
            return
        self.task.cancel()
        with suppress(asyncio.CancelledError):
            await self.task

    async def _run(self) -> None:
        activities = [Activity.idle, Activity.standing, Activity.walking, Activity.sitting]
        index = 0
        while True:
            await asyncio.sleep(1)
            self.tick += 1
            phase = self.tick % 16
            present = phase not in {0, 1, 2, 3}
            activity = activities[index % len(activities)] if present else Activity.idle
            if self.tick % 4 == 0:
                index += 1

            strength = max(0.05, min(1.0, 0.68 + 0.22 * math.sin(self.tick / 3)))
            confidence = 0.93 if present else 0.18
            rssi = -44 + 4 * math.sin(self.tick / 5)

            self.store.update_signal(
                strength=round(strength, 3),
                rssi_dbm=round(rssi, 1),
                channel=6,
                bandwidth_mhz=20,
            )
            await self.store.publish(
                Event(
                    event="signal.updated",
                    payload={
                        "strength": round(strength, 3),
                        "rssi_dbm": round(rssi, 1),
                        "channel": 6,
                        "bandwidth_mhz": 20,
                    },
                )
            )

            previous_count = self.store.state.presence.count
            self.store.update_presence(1 if present else 0, confidence)
            self.store.update_activity(activity)

            if present and previous_count == 0:
                await self.store.publish(
                    Event(
                        event="human.detected",
                        payload={"count": 1, "confidence": confidence, "activity": activity.value},
                    )
                )
            elif not present and previous_count > 0:
                await self.store.publish(
                    Event(
                        event="human.lost",
                        payload={"count": 0, "confidence": confidence},
                    )
                )

            await self.store.publish(
                Event(
                    event="activity.changed",
                    payload={"activity": activity.value, "confidence": round(confidence, 3)},
                )
            )
