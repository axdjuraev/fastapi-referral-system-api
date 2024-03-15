from datetime import datetime
from pydantic import BaseModel


class ReferralCodeSchemas(BaseModel):
    id: int
    code: str
    expires_at: datetime
    is_active: bool


class ReferralsSchemas(BaseModel):
    first_name: str
    last_name: str
    email: str
    referral_code_id: int
