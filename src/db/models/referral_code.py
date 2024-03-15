import sqlalchemy as sa
from .base import BaseModel
from .users import Users


class ReferralCode(BaseModel):
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    code = sa.Column(sa.String)
    expires_at = sa.Column(sa.DateTime)
    user_id = sa.Column(sa.ForeignKey(Users.id))
    is_active = sa.Column(sa.Boolean)
