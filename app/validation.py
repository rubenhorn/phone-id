from constants import SMS_PIN_LENGTH
import phonenumbers

class InputException(Exception):
    pass

def validate_and_format_phone_number(phone_number_str: str) -> str:
    parse_phone_number_exc = InputException('Invalid phone number')
    try:
        phone_number = phonenumbers.parse(phone_number_str, None)
    except phonenumbers.NumberParseException:
        raise parse_phone_number_exc
    if not phonenumbers.is_possible_number(phone_number):
        raise parse_phone_number_exc
    if not phonenumbers.is_valid_number(phone_number):
        raise parse_phone_number_exc
    return phonenumbers.format_number(phone_number, phonenumbers.PhoneNumberFormat.E164)

def validate_verification_code(verification_code: str):
    if not verification_code.isdigit() or len(verification_code) != SMS_PIN_LENGTH:
        raise InputException('Invalid verification code')
