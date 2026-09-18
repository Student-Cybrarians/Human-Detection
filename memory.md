# Project Memory

## Purpose
Maintain a concise record of architectural decisions and active work.

## What happened
- Repository default branch is master-branch.
- The previous frontend was removed from history; the current implementation is rebuilding the frontend and backend as a coherent vertical slice.
- Existing setup documentation described FastAPI + React/Vite, so this implementation preserves that direction.

## Currently working
- JARVIS command-center frontend.
- FastAPI realtime backend.
- Simulator-driven detection events.
- Contract and project documentation.

## Decisions
- API-first.
- WebSocket for realtime UI state.
- In-process event bus for MVP; Redis/NATS is a future scaling seam.
- SVG/CSS animation before introducing a heavy rendering engine.
- Raw CSI is not persisted by default.

## Next
1. Connect real CSI hardware through an ingestion adapter.
2. Add ML inference adapter.
3. Add persistent PostgreSQL state.
4. Add production authentication.
5. Add Cloudflare deployment after account/project configuration is verified.
