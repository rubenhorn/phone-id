import config
from constants import KEY_VONAGE_API_KEY, KEY_VONAGE_API_SECRET
import sys
from verification._abstract import PhoneVerificationService
from verification.mock import MockPhoneVerificationService
from verification.vonage import VonagePhoneVerificationService

def __create_phone_verification_service():
    vonage_api_key = config.get(KEY_VONAGE_API_KEY)
    vonage_api_secret = config.get(KEY_VONAGE_API_SECRET)
    if len(vonage_api_key) == 0 or len(vonage_api_secret) == 0:
        print('Incomplete Vonage configuration (Falling back on mock verification service)', file=sys.stderr)
        phone_verification_service = MockPhoneVerificationService()
    else:
        phone_verification_service = VonagePhoneVerificationService(vonage_api_key, vonage_api_secret)
    return phone_verification_service

__phone_verification_service = __create_phone_verification_service()

def get_phone_number_verification_service() -> PhoneVerificationService:
    return __phone_verification_service
