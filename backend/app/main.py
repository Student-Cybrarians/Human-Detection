from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

from .models import Event
from .simulator import DetectionSimulator
from .store import StateStore

store = StateStore()
simulator = DetectionSimulator(store)


@asynccontextmanager
async def lifespan(_: FastAPI):
    await simulator.start()
    yield
    await simulator.stop()


app = FastAPI(title="Human Detection JARVIS API", version="1.0.0", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health() -> dict:
    return {"status": "ok", "service": "human-detection-api"}


@app.get("/api/v1/state")
async def state():
    return store.snapshot()


@app.get("/api/v1/events")
async def events(limit: int = 25) -> list[Event]:
    limit = max(1, min(limit, 100))
    return list(store.events)[-limit:]


@app.post("/api/v1/simulator/step")
async def simulator_step():
    return {"status": "running", "message": "Simulator emits events continuously."}


@app.websocket("/ws")
async def websocket(websocket: WebSocket) -> None:
    await websocket.accept()
    queue = store.subscribe()
    try:
        snapshot = store.snapshot()
        await websocket.send_json(
            {
                "event": "system.online",
                "event_version": 1,
                "event_id": "system-initial",
                "timestamp": snapshot.last_event.timestamp.isoformat() if snapshot.last_event else None,
                "sequence": store.sequence,
                "payload": {"status": "online"},
            }
        )
        while True:
            event = await queue.get()
            await websocket.send_text(event.model_dump_json())
    except WebSocketDisconnect:
        pass
    finally:
        store.unsubscribe(queue)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
