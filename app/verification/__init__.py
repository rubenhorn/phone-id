from verification._abstract import PhoneVerificationService
from verification.mock import MockPhoneVerificationService

def __create_phone_verification_service():
    if True:#TODO use env vars
        phone_verification_service = MockPhoneVerificationService()
    return phone_verification_service

__phone_verification_service = __create_phone_verification_service()

def get_phone_verification_service() -> PhoneVerificationService:
    return __phone_verification_service
