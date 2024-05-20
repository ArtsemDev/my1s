from bcrypt import gensalt, checkpw, hashpw

__all__ = ["PasswordManager",]


class PasswordManager:

    @classmethod
    def create_password_hash(cls, password: str) -> str:
        salt = gensalt()
        return hashpw(password=password.encode(), salt=salt).decode()

    @classmethod
    def verity_password(cls, plain_password: str, hashed_password: str) -> bool:
        return checkpw(password=plain_password.encode(), hashed_password=hashed_password.encode())
