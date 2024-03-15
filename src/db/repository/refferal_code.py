from datetime import datetime
from src.db.schemas import RefferalCode as Schema
from src.db.schemas import ORefferalCode as OSchema
from src.db.models import ReferralCode as Model
from axsqlalchemy.repository import BaseRepository


class RefferalCodeRepository(BaseRepository[Model, Schema, OSchema]):
    async def all_active(self, date: datetime) -> list[OSchema]:
        return await self.all(
            filters=(
                (self.Model.is_active.is_(True)),
                (self.Model.expires_at > date).label('is_expired'),
            )
        )

    async def get_by_code(self, code: str) -> "OSchema | None":
        return await self.get(
            filters=(
                (self.Model.code == code),
            )
        )
