from __future__ import annotations

from dataclasses import dataclass
import numpy as np

@dataclass
class ProcessedCSI:
    tensor: np.ndarray

class CSIProcessor:
    def __init__(self, window_size: int = 32, channels: int = 2):
        self.window_size=window_size; self.channels=channels

    def transform(self, frames: list[np.ndarray]) -> ProcessedCSI:
        if not frames: return ProcessedCSI(np.zeros((self.channels,self.window_size),dtype=np.float32))
        x=np.asarray(frames,dtype=np.float32)
        if x.ndim==1: x=x[:,None]
        x=np.nan_to_num(x)
        x=(x-x.mean(axis=0,keepdims=True))/(x.std(axis=0,keepdims=True)+1e-6)
        if len(x)<self.window_size:
            x=np.pad(x,((self.window_size-len(x),0),(0,0)))
        else: x=x[-self.window_size:]
        x=x.T
        if x.shape[0]<self.channels: x=np.pad(x,((0,self.channels-x.shape[0]),(0,0)))
        return ProcessedCSI(x[:self.channels])
