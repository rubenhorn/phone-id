class VerificationException(Exception):
    pass
class VerificationCodeSendException(VerificationException):
    pass

class VerificationCodeCheckException(VerificationException):
    pass

class PhoneVerificationService():
        async def send_verification_code(self, phone_number) -> str:
            raise NotImplementedError()
            # TODO implement twilio or other verification api
            # raise VerificationCodeSendException('Phone number verification failed')

        async def verify_phone_number(self, phone_number, phone_number_verification_id, verification_code):
            raise NotImplementedError()
            # TODO implement twilio or other verification api
            # raise VerificationCodeCheckException('Phone number verification failed')