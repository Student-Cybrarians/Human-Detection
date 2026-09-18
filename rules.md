# Project Rules

## 1. What to use
- React 18 + Vite for the web UI.
- FastAPI + Pydantic for the backend.
- WebSocket for realtime events.
- CSS variables and SVG/CSS animation for the JARVIS core.
- Python pytest for backend tests; Vitest for frontend tests.
- API-first, contract-driven development.
- Small modules with explicit interfaces.

## 2. What to avoid
- Do not couple UI components directly to CSI or ML internals.
- Do not persist high-frequency raw CSI samples by default.
- Do not introduce microservices until a real scaling boundary exists.
- Do not use camera imagery as the primary human-detection mechanism.
- Do not put secrets in source control.
- Do not use unbounded event history in browser state.

## 3. Dependencies
Keep dependencies minimal. Prefer platform APIs and existing project dependencies over new libraries when practical. Pin major versions and document runtime requirements.

## 4. Error handling
- Backend returns structured HTTP errors.
- WebSocket failures must trigger reconnect with bounded exponential backoff.
- UI shows degraded/offline state rather than pretending sensing is active.
- Log server-side failures with request/event identifiers.

## 5. AI boundaries
AI/ML output is probabilistic. Never present confidence as certainty. Models may classify presence/activity; they must not infer identity, intent, emotion, or sensitive personal attributes.

## 6. General rules
- Python: 3.11+, type hints, Pydantic models, clear module boundaries.
- JavaScript: functional React components, stable keys, accessible controls.
- Naming: snake_case Python; camelCase JS; PascalCase React components.
- Tests must cover externally visible behavior.
- Prefer deterministic simulators for integration tests.
- Document architectural decisions and breaking event changes.
