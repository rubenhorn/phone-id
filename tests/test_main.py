from app.verification.mock import MockPhoneVerificationService
from fastapi.testclient import TestClient
import pytest
from starlette import responses

from main import app
from crud import recreate_database
from verification.mock import MockPhoneVerificationService

client = TestClient(app)

@pytest.fixture(scope='function')
def setup_run_teardown():
    recreate_database()
    yield

class TestRegister:
    def test_register_no_phone_number(self, setup_run_teardown):
        response = client.post('/register_number')
        # Expecting form in body
        assert response.status_code == 422

    def test_register_invalid_phone_number(self, setup_run_teardown):
        response = client.post('/register_number', json={ 'phone_number' : 'not a phone number' })
        assert response.status_code == 400

    def test_register_unverifiable_phone_number(self, setup_run_teardown):
        response = client.post('/register_number', json={ 
            'phone_number' : MockPhoneVerificationService.phone_number_cannot_send_verification_code
        })
        assert response.status_code == 500

    def test_register_phone_number(self, setup_run_teardown):
        body = { 'phone_number' : '+31 6 5555 1111' }
        response = client.post('/register_number', json=body)
        assert response.status_code == 201
        # Should not create a new user
        response = client.post('/register_number', json=body)
        assert response.status_code == 200

class TestRefresh:
    def test_refresh_no_token(self, setup_run_teardown):
        response = client.post('/refresh')
        # Expecting a refresh token in Authorization header
        assert response.status_code == 400
