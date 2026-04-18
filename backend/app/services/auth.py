import uuid
from passlib.context import CryptContext
from app.repositories.user import user_repository
from app.schemas.user import UserCreate

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


class AuthService:

    @staticmethod
    def get_password_hash(password: str) -> str:
        return pwd_context.hash(password)

    async def register_user(self, user_in: UserCreate):
        existing_user = await user_repository.get_by_email(user_in.email)
        if existing_user:
            raise ValueError("Email уже занят")

        user_data = user_in.model_dump()
        user_data["id"] = uuid.uuid4()
        password = user_data.pop("password")
        user_data["hashed_password"] = self.get_password_hash(password)

        created_user = await user_repository.create(user_data)
        return created_user


auth_service = AuthService()