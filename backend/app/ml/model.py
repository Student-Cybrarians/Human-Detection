from __future__ import annotations
import torch
from torch import nn

class CSIHumanModel(nn.Module):
    def __init__(self,n_channels=2,n_classes=6):
        super().__init__()
        self.encoder=nn.Sequential(nn.Conv1d(n_channels,32,5,padding=2),nn.ReLU(),nn.Conv1d(32,64,5,padding=2),nn.ReLU(),nn.AdaptiveAvgPool1d(1))
        self.presence=nn.Linear(64,2); self.activity=nn.Linear(64,n_classes)
    def forward(self,x):
        z=self.encoder(x).squeeze(-1)
        return self.presence(z),self.activity(z)
