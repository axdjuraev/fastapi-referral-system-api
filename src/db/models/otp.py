import sqlalchemy as sa
from .base import BaseModel


class OtpCode(BaseModel):
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    email = sa.Column(sa.String)
    code = sa.Column(sa.String)
    is_active = sa.Column(sa.Boolean)
