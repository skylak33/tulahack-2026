from app.database.db import database
from app.database.models import users
import uuid
import sqlalchemy

class UserRepository:
    async def get_by_email(self, email: str):
        query = users.select().where(users.c.email == email)
        return await database.fetch_one(query)

    async def get_by_id(self, user_id: uuid.UUID):
        query = users.select().where(users.c.id == user_id)
        return await database.fetch_one(query)

    async def create(self, user_data: dict):
        query = users.insert().values(**user_data).returning(users)
        return await database.fetch_one(query)

    async def update(self, user_id: uuid.UUID, data: dict):
        query = users.update().where(users.c.id == user_id).values(**data).returning(users)
        return await database.fetch_one(query)

    async def delete(self, user_id: uuid.UUID) -> None:
        query = users.delete().where(users.c.id == user_id)
        await database.execute(query)

    async def get_all(
        self,
        role: str | None = None,
        team_role: str | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> tuple[int, list]:
        base = users.select()
        count_base = sqlalchemy.select(sqlalchemy.func.count()).select_from(users)

        if role:
            base = base.where(users.c.role == role)
            count_base = count_base.where(users.c.role == role)
        if team_role:
            base = base.where(users.c.team_role == team_role)
            count_base = count_base.where(users.c.team_role == team_role)

        total = await database.fetch_val(count_base)
        items = await database.fetch_all(base.limit(limit).offset(offset))
        return total, items


user_repository = UserRepository()