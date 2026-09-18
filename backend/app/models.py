from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from uuid import uuid4

from pydantic import BaseModel, Field


class Activity(str, Enum):
    idle = "idle"
    standing = "standing"
    walking = "walking"
    running = "running"
    sitting = "sitting"
    fall = "fall"


class Signal(BaseModel):
    channel: int = 6
    bandwidth_mhz: int = 20
    rssi_dbm: float = -48
    noise_floor_dbm: float = -92
    strength: float = Field(0.82, ge=0, le=1)


class Presence(BaseModel):
    count: int = Field(0, ge=0)
    confidence: float = Field(0, ge=0, le=1)


class Event(BaseModel):
    event: str
    event_version: int = 1
    event_id: str = Field(default_factory=lambda: f"evt_{uuid4().hex[:12]}")
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    sequence: int = 0
    payload: dict


class Device(BaseModel):
    id: str
    name: str
    zone: str
    status: str
    signal_strength: float = Field(0.0, ge=0, le=1)


class JarvisState(BaseModel):
    status: str = "online"
    presence: Presence = Field(default_factory=Presence)
    activity: Activity = Activity.idle
    signal: Signal = Field(default_factory=Signal)
    devices: list[Device] = Field(default_factory=list)
    alerts: list[dict] = Field(default_factory=list)
    last_event: Event | None = None
