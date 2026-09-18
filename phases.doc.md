# Delivery Phases

## Phase 1 — Authentication & access foundation
- Establish runtime configuration.
- Add health/readiness endpoints.
- Define future auth seam for operator/device identities.

## Phase 2 — JARVIS dashboard
- Build command-center layout.
- Implement animated core.
- Add signal, presence, activity, devices and alerts panels.
- Add responsive and reduced-motion behavior.

## Phase 3 — Realtime detection
- Define versioned domain events.
- Implement WebSocket connection lifecycle.
- Add deterministic CSI simulator.
- Connect simulator -> backend -> browser without polling.

## Phase 4 — Detection operations
- Add activity timeline.
- Add alert creation/acknowledgement.
- Add device status.
- Add bounded event history.

## Phase 5 — Quality assurance
- Backend unit/integration tests.
- Frontend component tests.
- WebSocket reconnect tests.
- Production builds.
- CI checks.

## Phase 6 — Deployment & maintenance
- Docker deployment.
- Cloudflare static frontend configuration.
- Origin API deployment.
- Observability and rollback procedure.
- Replace simulator with hardware adapter without changing domain events.
