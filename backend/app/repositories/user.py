from app.database.db import database
from app.database.models import users

class UserRepository:
    async def get_by_email(self, email: str):
        query = users.select().where(users.c.email == email)
        return await database.fetch_one(query)

    async def create(self, user_data: dict):
        query = users.insert().values(**user_data).returning(users)
        return await database.fetch_one(query)

user_repository = UserRepository()