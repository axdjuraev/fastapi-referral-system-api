from abc import ABC, abstractmethod


class CodeGenerator(ABC):
    @abstractmethod
    def generate_otp(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def generate_referral_code(self) -> str:
        raise NotImplementedError
