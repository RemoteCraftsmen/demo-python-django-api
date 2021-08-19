from random import randbytes


class PasswordResetTokenGeneratorHandler:
    @staticmethod
    def handle():
        return randbytes(64).hex()
