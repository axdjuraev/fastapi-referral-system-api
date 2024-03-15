from pydantic import EmailStr
from fastapi.security import OAuth2PasswordRequestForm
from .base import BaseModel


class LoginInfoSchemas(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr

    class Config:
        orm_mode = True


class RegistraionSchemas(LoginInfoSchemas):
    password: str


class LoginSchemas(OAuth2PasswordRequestForm):
    username: EmailStr
    password: str


class LoginPayloadSchema(BaseModel):
    user: LoginInfoSchemas
    access_token: str
    refresh_token: str
