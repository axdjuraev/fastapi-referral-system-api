from datetime import datetime
from pydantic import BaseModel


class ReferralCodeSchemas(BaseModel):
    id: int
    code: str
    expires_at: datetime
    user_id: int
    is_active: bool
