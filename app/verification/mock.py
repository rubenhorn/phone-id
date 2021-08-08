from constants import SMS_PIN_LENGTH
import phonenumbers
from verification.abc import PhoneVerificationService
from verification.exceptions import VerificationCodeSendException, VerificationCodeCheckException

class MockPhoneVerificationService(PhoneVerificationService):

    phone_number_cannot_send_verification_code = phonenumbers.parse('+31 6 5555 5555', None)
    phone_number_verification_id = 'mock_phone_number_verification_id'
    verification_code_valid = '0' * SMS_PIN_LENGTH

    async def send_verification_code(self, phone_number) -> str:
            if phonenumbers.parse(phone_number, None) == self.phone_number_cannot_send_verification_code:
                raise VerificationCodeSendException()
            else:
                return self.phone_number_verification_id

    async def verify_phone_number(self, phone_number, phone_number_verification_id, verification_code):
        if verification_code != self.verification_code_valid:
            raise VerificationCodeCheckException()

    async def cancel_phone_number_verification(self, phone_number_verification_id):
        pass        
