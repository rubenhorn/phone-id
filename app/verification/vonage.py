from constants import SMS_PIN_LENGTH
import sys
from verification.abc import PhoneVerificationService
from verification.exceptions import VerificationCodeSendException, VerificationCodeCheckException
import vonage

class VonagePhoneVerificationService(PhoneVerificationService):
    def __init__(self, api_key, api_secret):
        client = vonage.Client(api_key, api_secret)
        self.verify = vonage.Verify(client)

    async def send_verification_code(self, phone_number) -> str:
        response = self.verify.start_verification(number=phone_number, code_length=SMS_PIN_LENGTH, brand='CollAction App', sender_id='CollAction')
        if response['status'] == '0':
            return response['request_id']
        else:
            error_text = response['error_text']
            print(f'Error starting verification: {error_text}', file=sys.stderr)
            raise VerificationCodeSendException('Phone number verification failed')

    async def verify_phone_number(self, phone_number, phone_number_verification_id, verification_code):
        response = self.verify.check(phone_number_verification_id, code=verification_code)
        if response['status'] != '0':
            error_text = response['error_text']
            print(f'Error on verification check: {error_text}', file=sys.stderr)
            raise VerificationCodeCheckException('Phone number verification failed')

    async def cancel_phone_number_verification(self, phone_number_verification_id):
        response = self.verify.cancel(phone_number_verification_id)
        if response['status'] != '0':
            error_text = response['error_text']
            print(f'Error canceling verification: {error_text}', file=sys.stderr)
        
