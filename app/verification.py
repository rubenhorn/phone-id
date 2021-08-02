class VerificationException(Exception):
    pass
class VerificationCodeSendException(VerificationException):
    pass

class VerificationCodeCheckException(VerificationException):
    pass


async def send_verification_code(phone_number) -> str:
    # TODO implement twilio or other verification api
    # raise VerificationCodeSendException('Phone number verification failed')
    return 'myVerificationId'

async def verify_phone_number(phone_number, phone_number_verification_id, verification_code):
    # TODO implement twilio or other verification api
    # raise VerificationCodeCheckException('Phone number verification failed')
    pass
