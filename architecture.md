# Architecture

## System overview

~~~mermaid
flowchart LR
  Sensor[WiFi / CSI Sensor] --> Ingest[CSI Ingestion]
  Ingest --> Features[Preprocess + Feature Extraction]
  Features --> Inference[Human / Activity Inference]
  Inference --> Domain[Domain Event Publisher]
  Domain --> API[FastAPI REST]
  Domain --> WS[WebSocket Realtime Hub]
  API --> UI[JARVIS React UI]
  WS --> UI
  Domain --> Store[(State Store)]
~~~

The first implementation uses an in-process event bus and in-memory state. The interface is intentionally shaped so Redis Streams/PostgreSQL can be introduced later without changing the frontend event contract.

## Modules
- ingestion: accepts simulated or real CSI observations.
- inference: converts observations to presence/activity predictions.
- domain: owns event names and normalized state.
- api: REST resources and WebSocket transport.
- frontend: consumes REST + WebSocket only; it does not know CSI internals.
- store: current state and bounded recent events.

## Event contract
Every realtime event contains:
- event
- event_version
- event_id
- timestamp
- sequence
- payload

Primary events:
- system.online
- human.detected
- human.lost
- activity.changed
- signal.updated
- alert.created
- device.updated

## Frontend state machine
~~~text
connecting -> connected -> sensing
                 |           |
                 v           v
             reconnecting <- disconnected
~~~

Detection animation is derived from state, never from arbitrary component timers.

## Deployment
Local/default:
- React/Vite on :5173
- FastAPI on :8000
- Docker Compose available for both.

Cloud deployment:
- Static frontend can target Cloudflare Pages/Workers.
- FastAPI remains an origin service unless converted to a Cloudflare-compatible runtime.
- WebSocket origin must be explicitly configured and authenticated.

## Scaling seam
For multiple sensors or processes, replace the in-process publisher/store with Redis Streams or NATS and move state persistence to PostgreSQL/TimescaleDB. The event schema remains stable.
