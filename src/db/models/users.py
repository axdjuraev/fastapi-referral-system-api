import sqlalchemy as sa
from .base import BaseModel


class Users(BaseModel):
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    first_name = sa.Column(sa.String)
    last_name = sa.Column(sa.String)
    email = sa.Column(sa.String)
    password_hash = sa.Column(sa.String)
    referral_code_id = sa.Column(sa.String, nullable=True)
