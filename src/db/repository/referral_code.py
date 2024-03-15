from datetime import datetime
from src.db.schemas import ReferralCode as Schema
from src.db.schemas import OReferralCode as OSchema
from src.db.models import ReferralCode as Model
from axsqlalchemy.repository import BaseRepository


class ReferralCodeRepository(BaseRepository[Model, Schema, OSchema]):
    async def all_by_user(self, user_id):
        return await self.all(
            filters=(
                (self.Model.user_id == user_id),
            )
        )

    async def all_active_by_user(self, user_id, date: datetime) -> list[OSchema]:
        return await self.all(
            filters=(
                (self.Model.is_active.is_(True)),
                (self.Model.expires_at > date).label('is_expired'),
                (self.Model.user_id == user_id),
            )
        )

    async def get_by_code(self, code: str) -> "OSchema | None":
        return await self.get(
            filters=(
                (self.Model.code == code),
            )
        )
