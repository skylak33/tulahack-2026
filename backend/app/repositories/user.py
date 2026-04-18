from app.database.db import database
from app.database.models import users
import uuid

class UserRepository:
    async def get_by_email(self, email: str):
        query = users.select().where(users.c.email == email)
        return await database.fetch_one(query)

    async def create(self, user_data: dict):
        query = users.insert().values(**user_data).returning(users)
        return await database.fetch_one(query)

    async def get_by_id(self, user_id: uuid.UUID):
        query = users.select().where(users.c.id == user_id)
        return await database.fetch_one(query)

user_repository = UserRepository()