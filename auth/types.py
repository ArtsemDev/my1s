from pydantic import BaseModel, EmailStr, model_validator

from src.annotated_types import PasswordStr

__all__ = ["UserLogin", "UserRegister"]


class UserLogin(BaseModel):
    email: EmailStr
    password: PasswordStr


class UserRegister(UserLogin):
    confirm_password: PasswordStr

    @model_validator(mode="after")
    def validate_passwords(self):
        assert self.password == self.confirm_password
        return self
