from src.db.schemas import OTPCode as Schema
from src.db.models import OTPCode as Model
from axsqlalchemy.repository import BaseRepository


class OTPCodeRepository(BaseRepository[Model, Schema, Schema]):
    async def get_by_code_and_email(self, code: str, email: str) -> "Schema | None":
        return await self.get(
            filters=(
                (self.Model.code == code),
                (self.Model.email == email),
                (self.Model.is_active.is_(True)),
            )
        )
