from .base import BaseModel


class Users(BaseModel):
    first_name: str
    last_name: str
    email: str
    password_hash: str


class OUsers(Users):
    id: int
