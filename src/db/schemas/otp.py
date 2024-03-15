from typing import Optional
from .base import BaseModel


class OTPCode(BaseModel):
    id: Optional[int] = None
    email: str
    code: str
