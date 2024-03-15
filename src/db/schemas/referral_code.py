from datetime import datetime
from typing import Optional
from .base import BaseModel


class ReferralCode(BaseModel):
    code: str
    expires_at: datetime
    user_id: int
    is_active: bool

    def is_expired(self, date: Optional[datetime] = None) -> bool:
        if not date:
            date = datetime.now()

        return (self.expires_at - date).seconds <= 0


class OReferralCode(ReferralCode):
    id: int
