from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_stream_updates():
    response = client.get("/v1/stream/")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/event-stream"
