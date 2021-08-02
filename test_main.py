from fastapi import FastAPI
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

def test_refresh_no_token():
    response = client.post('/refresh')
    # Expecting a refresh token in Authorization header
    assert response.status_code == 400
