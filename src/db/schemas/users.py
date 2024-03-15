from typing import Optional
from .base import BaseModel


class Users(BaseModel):
    first_name: str
    last_name: str
    email: str
    password_hash: str
    referral_code_id: Optional[str] = None


class OUsers(Users):
    id: int
