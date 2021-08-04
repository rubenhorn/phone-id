from fastapi.testclient import TestClient
import pytest

from main import app
from crud import recreate_database

client = TestClient(app)

@pytest.fixture(scope='function')
def setup_run_teardown():
    recreate_database()
    yield

class TestRefresh:
    def test_refresh_no_token(self, setup_run_teardown):
        response = client.post('/refresh')
        # Expecting a refresh token in Authorization header
        assert response.status_code == 400
