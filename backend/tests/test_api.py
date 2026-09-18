from fastapi.testclient import TestClient

from app.main import app


def test_health() -> None:
    with TestClient(app) as client:
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "ok"


def test_state_contract() -> None:
    with TestClient(app) as client:
        response = client.get("/api/v1/state")
        body = response.json()
        assert "presence" in body
        assert "signal" in body
        assert "devices" in body


def test_websocket_receives_system_event() -> None:
    with TestClient(app) as client:
        with client.websocket_connect("/ws") as websocket:
            message = websocket.receive_json()
            assert message["event"] == "system.online"
            assert message["event_version"] == 1
