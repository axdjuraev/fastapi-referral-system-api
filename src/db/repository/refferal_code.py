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
                ((date - self.Model.expires_at) <= 0),
            )
        )
