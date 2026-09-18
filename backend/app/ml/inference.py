from __future__ import annotations
from dataclasses import dataclass
import numpy as np
import torch
from .model import CSIHumanModel
from .preprocessing import CSIProcessor

@dataclass
class InferenceResult:
    present: bool
    presence_confidence: float
    activity: str
    activity_confidence: float
    model: str="jarvis-csi-pytorch"
    version: str="0.1.0"
    distance_m: float|None=None
    distance_confidence: float|None=None
    pose_available: bool=False
    skeleton: list[dict]=None

class RealtimeInference:
    activities=["idle","standing","walking","running","sitting","fall"]
    def __init__(self):
        self.processor=CSIProcessor(); self.model=CSIHumanModel(); self.model.eval()
    def predict(self,frames:list[np.ndarray])->InferenceResult:
        x=torch.from_numpy(self.processor.transform(frames).tensor).unsqueeze(0)
        with torch.inference_mode():
            p,a=self.model(x); pp=torch.softmax(p,1)[0]; aa=torch.softmax(a,1)[0]
        pi=int(torch.argmax(pp)); ai=int(torch.argmax(aa))
        return InferenceResult(bool(pi),float(pp[pi]),self.activities[ai],float(aa[ai]),skeleton=[])
