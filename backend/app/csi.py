from __future__ import annotations
from dataclasses import dataclass
import math
import numpy as np

@dataclass
class CSIFrame:
    amplitude: np.ndarray
    phase: np.ndarray
    timestamp: float
    source: str="simulator"

class CSIAdapter:
    async def read(self)->CSIFrame: raise NotImplementedError

class SimulatedCSIAdapter(CSIAdapter):
    def __init__(self): self.t=0
    async def read(self):
        self.t+=0.05; n=64; idx=np.arange(n)
        amp=1+0.25*np.sin(idx*.3+self.t*2)+0.08*np.sin(self.t*7)
        phase=np.unwrap(0.3*np.sin(idx*.12+self.t))
        return CSIFrame(amp.astype(np.float32),phase.astype(np.float32),self.t)
