class VerificationException(Exception):
    pass

class VerificationCodeSendException(VerificationException):
    pass

class VerificationCodeCheckException(VerificationException):
    pass