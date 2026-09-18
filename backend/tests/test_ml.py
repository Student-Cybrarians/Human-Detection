import numpy as np
from app.ml.preprocessing import CSIProcessor
from app.ml.inference import RealtimeInference

def test_processor_shape_and_finite():
    x=CSIProcessor(window_size=32).transform([np.array([1.,2.,3.])]).tensor
    assert x.shape==(2,32); assert np.isfinite(x).all()

def test_realtime_inference_contract():
    r=RealtimeInference().predict([np.ones(64,dtype=np.float32) for _ in range(32)])
    assert 0 <= r.presence_confidence <= 1
    assert r.activity in RealtimeInference.activities
    assert r.distance_m is None
    assert r.pose_available is False
