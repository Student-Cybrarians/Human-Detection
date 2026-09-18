from __future__ import annotations
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from .models import Event
from .simulator import DetectionSimulator
from .store import StateStore
store=StateStore(); simulator=DetectionSimulator(store)
@asynccontextmanager
async def lifespan(_:FastAPI):
    await simulator.start(); yield; await simulator.stop()
app=FastAPI(title="Human Detection JARVIS API",version="2.0.0",lifespan=lifespan)
origins=[x.strip() for x in os.getenv("CORS_ORIGINS","http://localhost:5173,https://human-detection.pages.dev").split(",") if x.strip()]
app.add_middleware(CORSMiddleware,allow_origins=origins,allow_credentials=False,allow_methods=["GET","POST"],allow_headers=["*"])
@app.get("/health")
async def health(): return {"status":"ok","service":"human-detection-api","mode":"simulator","ml":"pytorch"}
@app.get("/api/v1/state")
async def state(): return store.snapshot()
@app.get("/api/v1/events")
async def events(limit:int=25)->list[Event]: return list(store.events)[-max(1,min(limit,100)):]
@app.post("/api/v1/simulator/step")
async def simulator_step(): return {"status":"running","mode":"simulator","message":"CSI simulator feeds the PyTorch inference pipeline continuously."}
@app.websocket("/ws")
async def websocket(websocket:WebSocket):
    await websocket.accept(); queue=store.subscribe()
    try:
        await websocket.send_json({"event":"system.online","event_version":1,"event_id":"system-initial","sequence":store.sequence,"payload":{"status":"online","source":"simulator","ml":"pytorch"}})
        while True: await websocket.send_text((await queue.get()).model_dump_json())
    except WebSocketDisconnect: pass
    finally: store.unsubscribe(queue)
if __name__=="__main__":
    import uvicorn; uvicorn.run("app.main:app",host="0.0.0.0",port=8000)
