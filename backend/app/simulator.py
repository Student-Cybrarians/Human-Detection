from __future__ import annotations

import asyncio, math
from contextlib import suppress
import numpy as np
from .models import Activity, Event
from .store import StateStore
from .csi import SimulatedCSIAdapter
from .ml.inference import RealtimeInference

class DetectionSimulator:
    """Development CSI source. It is explicitly marked simulator and uses the same ML inference path."""
    def __init__(self, store: StateStore) -> None:
        self.store=store; self.tick=0; self.task=None; self.adapter=SimulatedCSIAdapter(); self.inference=RealtimeInference(); self.frames=[]; self.last_present=False; self.last_activity=None
    async def start(self):
        if self.task and not self.task.done(): return
        self.task=asyncio.create_task(self._run())
    async def stop(self):
        if not self.task:return
        self.task.cancel()
        with suppress(asyncio.CancelledError): await self.task
    async def _run(self):
        while True:
            await asyncio.sleep(0.05); self.tick+=1
            frame=await self.adapter.read(); self.frames.append(frame.amplitude); self.frames=self.frames[-32:]
            result=self.inference.predict(self.frames)
            # Simulator remains visibly marked; untrained range/pose are intentionally unavailable.
            signal=float(np.clip(np.mean(frame.amplitude)/2,0,1)); rssi=-44+4*math.sin(self.tick/20)
            self.store.update_signal(strength=round(signal,3),rssi_dbm=round(rssi,1),channel=6,bandwidth_mhz=20)
            await self.store.publish(Event(event="signal.updated",payload={"strength":round(signal,3),"rssi_dbm":round(rssi,1),"channel":6,"bandwidth_mhz":20,"source":"simulator"}))
            present=result.present; activity=Activity(result.activity)
            self.store.update_presence(int(present),result.presence_confidence); self.store.update_activity(activity)
            if present and not self.last_present:
                await self.store.publish(Event(event="human.detected",payload={"count":1,"confidence":result.presence_confidence,"activity":result.activity,"activity_confidence":result.activity_confidence,"distance_m":None,"distance_confidence":None,"pose_available":False,"skeleton":[],"source":"simulator","model":{"name":result.model,"version":result.version}}))
            elif not present and self.last_present:
                await self.store.publish(Event(event="human.lost",payload={"count":0,"confidence":result.presence_confidence,"source":"simulator"}))
            if activity != self.last_activity:
                await self.store.publish(Event(event="activity.changed",payload={"activity":result.activity,"confidence":result.activity_confidence,"source":"simulator","model":result.model}))
            self.last_present=present; self.last_activity=activity
