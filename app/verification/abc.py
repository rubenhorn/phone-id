from abc import ABC, abstractmethod

class PhoneVerificationService(ABC):
    @abstractmethod
    async def send_verification_code(self, phone_number) -> str:
        pass

    @abstractmethod
    async def verify_phone_number(self, phone_number, phone_number_verification_id, verification_code):
        pass

    @abstractmethod
    async def cancel_phone_number_verification(self, phone_number_verification_id):
        pass
