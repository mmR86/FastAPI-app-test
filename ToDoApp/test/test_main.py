from fastapi import status
from fastapi.testclient import TestClient

from ..main import app

# It lets you send HTTP requests to your FastAPI application directly from Python tests, without having to start a real web server.
client = TestClient(app)

def test_return_health_check():
    response = client.get("/healthy")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "Healthy"}