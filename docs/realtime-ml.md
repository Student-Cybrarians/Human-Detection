# Realtime ML backend

The backend now has a PyTorch inference seam: CSI adapter -> preprocessing -> temporal window -> presence/activity model -> domain events -> WebSocket.

## Current mode

The development path uses `SimulatedCSIAdapter`. It is explicitly marked `source=simulator`. The PyTorch checkpoint is currently an untrained architecture, so predictions are an ML pipeline smoke-test rather than validated human detection.

## Real hardware

Implement a `CSIAdapter` for the selected CSI-capable NIC/ESP32 capture format. Feed calibrated amplitude/phase frames into the same processor. A trained checkpoint must be loaded before interpreting predictions as validated detection results.

## Distance and pose

Range estimation requires labeled, calibrated CSI data and fixed antenna/link geometry. Pose requires a validated CSI pose model and suitable spatial diversity. Until these are configured, the API returns `distance_m=null` and `pose_available=false`; the UI must not invent measurements.
