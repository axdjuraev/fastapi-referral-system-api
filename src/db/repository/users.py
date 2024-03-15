from src.db.schemas import Users as Schema
from src.db.schemas import OUsers as OSchema
from src.db.models import UsersModel as Model
from axsqlalchemy.repository import BaseRepository


class UsersRepository(BaseRepository[Model, Schema, OSchema]):
    async def get_by_email(self, email: str) -> "OSchema | None":
        return await self.get(
            filters=(
                (self.Model.email == email),
            )
        )
