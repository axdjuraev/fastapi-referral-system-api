from datetime import datetime
from .base import BaseModel


class RefferalCode(BaseModel):
    code: str
    expires_at: datetime
    user_id: int
    is_active: bool


class ORefferalCode(RefferalCode):
    id: int
