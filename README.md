# Human Detection — JARVIS

Privacy-first WiFi/CSI human sensing with a realtime JARVIS command center.

## Architecture
~~~text
CSI / Simulator -> FastAPI -> Domain Events -> WebSocket -> React JARVIS UI
~~~

The frontend does not depend on CSI implementation details. It consumes a versioned event contract.

## Quick start

### Backend
~~~bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
~~~

### Frontend
~~~bash
cd frontend
npm install
npm run dev
~~~

Open http://localhost:5173.

The backend simulator starts with the API and emits deterministic signal/presence/activity changes so the UI can be exercised without hardware.

## Docker
~~~bash
docker compose up --build
~~~

## Documentation
- PRD: ./PRD.md
- Architecture: ./architecture.md
- Rules: ./rules.md
- Delivery phases: ./phases.doc.md
- Design system: ./design.md
- Project memory: ./memory.md
- Setup guide: ./docs/setup.md

## Agentic workflow
The implementation follows API-first and contract-driven guidance from Agentic Awesome Skills, particularly backend architecture and full-stack orchestration. The external skill catalog is guidance; it is not a runtime dependency.
