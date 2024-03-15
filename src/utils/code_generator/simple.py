import random
from .base import CodeGenerator


class SimpleCodeGenerator(CodeGenerator):
    def _generate_random_value(self):
        return str(random.randint(100000, 9999999))

    def generate_otp(self):
        return self._generate_random_value()

    def generate_referral_code(self):
        return self._generate_random_value()
