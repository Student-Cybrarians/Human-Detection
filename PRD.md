# PRD — WiFi Human Detection / JARVIS

## 1. What to build
A privacy-first WiFi/CSI human-detection command center. The product turns CSI/signal observations into human-presence and activity events and presents them through a cinematic JARVIS interface.

### Goals
- Detect human presence without a camera in the primary sensing path.
- Surface presence, activity, confidence, signal health, devices and alerts in real time.
- Keep the UI decoupled from CSI/ML implementation details through versioned domain events.
- Provide a deterministic simulator so the complete vertical slice works before hardware is connected.

## 2. Target users
- Researchers and students building WiFi sensing systems.
- Operators monitoring a room or lab.
- Developers integrating CSI hardware and ML models.

## 3. Core features
- JARVIS Core visualization with state-driven animation.
- Real-time WebSocket event stream.
- Presence count and confidence.
- Activity state: idle, standing, walking, running, sitting, fall.
- CSI signal waveform visualization.
- Device health and connection state.
- Activity timeline and alerts.
- REST health/state endpoints.
- Deterministic CSI/signal simulator.
- Reduced-motion accessibility mode.

## 4. Success criteria
- Simulator can emit a human-detected event and the UI changes state without refresh.
- WebSocket reconnects and resumes subscriptions.
- API and event contracts are documented.
- Frontend production build succeeds.
- Backend tests cover health, state and WebSocket event flow.
- No camera data is required by the core detection path.

## 5. Non-goals for this phase
- Production-grade ML training.
- Raw CSI long-term storage.
- Multi-tenant billing.
- Cloud-scale orchestration.
- Automatic Cloudflare deployment without verified account/project configuration.

## 6. Privacy and safety
CSI measurements are treated as sensing data. The application must minimize retention, avoid storing raw signal streams by default, expose confidence and source metadata, and never claim certainty beyond the model output.
