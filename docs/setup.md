# WiFi Human Detection / JARVIS Setup

## Prerequisites
- Python 3.11+
- Node.js 20+
- Docker + Docker Compose (optional)

## Docker
~~~bash
docker compose up --build
~~~
- Frontend: http://localhost:5173
- Backend: http://localhost:8000
- API docs: http://localhost:8000/docs
- WebSocket: ws://localhost:8000/ws

## Backend
~~~bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
~~~

Tests:
~~~bash
cd backend
pytest -q
~~~

## Frontend
~~~bash
cd frontend
npm install
npm run dev
~~~

Build:
~~~bash
npm run build
~~~

Set the API origin with VITE_API_URL in frontend/.env.local.

## Realtime contract
The browser consumes versioned events from /ws:
- system.online
- human.detected
- human.lost
- activity.changed
- signal.updated

Every event has event_version, event_id, timestamp, sequence, and payload.

## Simulator
The FastAPI lifespan starts a deterministic simulator automatically. This gives the frontend a complete sensing loop without real hardware.

Replace backend/app/simulator.py with a hardware/ML adapter when CSI ingestion is ready. Keep the domain event contract unchanged.

## Cloudflare
See cloudflare.md for Cloudflare Pages deployment of the frontend and the origin/WebSocket requirements.

## Security
The MVP uses permissive local CORS and has no user authentication. Before public deployment:
1. Restrict CORS.
2. Add operator/device authentication.
3. Protect WebSocket subscriptions.
4. Move secrets to environment/secret storage.
5. Add persistent audit logging.
