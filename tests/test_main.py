from app.verification.mock import MockPhoneVerificationService
from base64 import b64decode
from fastapi.testclient import TestClient
import json
import pytest
from main import app
from crud import recreate_database
import time
from verification.mock import MockPhoneVerificationService

client = TestClient(app)

phone_number_valid = '+31655551111'

@pytest.fixture(scope='function')
def setup_run_teardown():
    assert phone_number_valid != MockPhoneVerificationService.phone_number_cannot_send_verification_code
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
        body = { 'phone_number' : phone_number_valid }
        response = client.post('/register_number', json=body)
        assert response.status_code == 201
        # Should not create a new user
        response = client.post('/register_number', json=body)
        assert response.status_code == 200

class TestVerify:
    def test_verify_no_phone_number_no_code(self, setup_run_teardown):
        response = client.post('/verify_number', json={})
        assert response.status_code == 422

    def test_verify_no_phone_number(self, setup_run_teardown):
        response = client.post('/verify_number', json={ 'verification_code' : '12345' })
        assert response.status_code == 422

    def test_verify_no_code(self, setup_run_teardown):
        response = client.post('/verify_number', json={ 'phone_number' : phone_number_valid })
        assert response.status_code == 422

    def test_verify_user_does_not_exist(self, setup_run_teardown):
        response = client.post('/verify_number', json={ 'phone_number' : phone_number_valid, 'verification_code' : '123456' })
        assert response.status_code == 404

    def test_verify_invalid_code(self, setup_run_teardown):
        client.post('/register_number', json={ 'phone_number' : phone_number_valid })
        code = '123456'
        assert code != MockPhoneVerificationService.verification_code_valid
        response = client.post('/verify_number', json={ 'phone_number' : phone_number_valid, 'verification_code' : code })
        assert response.status_code == 422

    def test_verify_code_is_valid(self, setup_run_teardown):
        client.post('/register_number', json={ 'phone_number' : phone_number_valid })
        code = MockPhoneVerificationService.verification_code_valid
        response = client.post('/verify_number', json={ 'phone_number' : phone_number_valid, 'verification_code' : code })
        assert response.status_code == 200
        # Check accsess token
        access_token = response.json()['access_token']
        access_token_claims = json.loads(b64decode(access_token.split('.')[1]))
        assert access_token_claims['type'] == 'access'
        assert 'sub' in access_token_claims
        assert 'jti' in access_token_claims
        assert access_token_claims['phone_number'] == phone_number_valid
        assert access_token_claims['phone_number_verified'] == True
        # Check refresh token
        refresh_token = response.json()['refresh_token']
        refresh_token_claims = json.loads(b64decode(refresh_token.split('.')[1]))
        assert refresh_token_claims['type'] == 'refresh'
        assert 'sub' in refresh_token_claims
        assert 'jti' in refresh_token_claims
        assert refresh_token_claims['phone_number'] == phone_number_valid
        assert refresh_token_claims['phone_number_verified'] == True

class TestRefresh:
    def test_refresh_no_token(self, setup_run_teardown):
        response = client.post('/refresh')
        # Expecting a refresh token in Authorization header
        assert response.status_code == 400

    def test_refresh_invalid_token(self, setup_run_teardown):
        response = client.post('/refresh', headers={ 'Authorization' : 'Bearer not a token' })
        assert response.status_code == 400

    def test_refresh_token_is_valid(self, setup_run_teardown):
        client.post('/register_number', json={ 'phone_number' : phone_number_valid })
        code = MockPhoneVerificationService.verification_code_valid
        response = client.post('/verify_number', json={ 'phone_number' : phone_number_valid, 'verification_code' : code })
        access_token = response.json()['access_token']
        initial_claims = json.loads(b64decode(access_token.split('.')[1]))
        refresh_token = response.json()['refresh_token']
        time.sleep(1) # Make sure that a different token will be generated
        response = client.post('/refresh', headers={ 'Authorization' : 'Bearer ' + refresh_token })
        assert response.status_code == 200
        assert access_token != response.json()['access_token']
        # Check if the token has the same claims
        access_token = response.json()['access_token']
        new_claims = json.loads(b64decode(access_token.split('.')[1]))
        assert new_claims['type'] == 'access'
        assert new_claims['sub'] == initial_claims['sub']
        assert new_claims['jti'] != initial_claims['jti'] # JTI is unique
        assert new_claims['phone_number'] == initial_claims['phone_number']
        assert new_claims['phone_number_verified'] == initial_claims['phone_number_verified']
        
