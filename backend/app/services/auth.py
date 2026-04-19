import uuid
import jwt
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from app.repositories.user import user_repository
from app.schemas.user import UserCreate
from app.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


class AuthService:
    @staticmethod
    def get_password_hash(password: str) -> str:
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    def create_token(self, data: dict, expires_delta: timedelta) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + expires_delta
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    async def register_user(self, user_in: UserCreate):
        existing_user = await user_repository.get_by_email(user_in.email)
        if existing_user:
            raise ValueError("Email уже занят")

        user_data = user_in.model_dump()
        user_data["id"] = uuid.uuid4()
        password = user_data.pop("password")
        user_data["hashed_password"] = self.get_password_hash(password)
        return await user_repository.create(user_data)

    async def authenticate_user(self, email: str, password: str):
        user = await user_repository.get_by_email(email)
        if not user or not self.verify_password(password, user["hashed_password"]):
            return None
        return user

    def refresh_access_token(self, refresh_token: str) -> str:
        try:
            payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
            user_id = payload.get("sub")
            if not user_id:
                raise ValueError("Invalid token")
            return self.create_token(
                data={"sub": user_id},
                expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
            )
        except jwt.PyJWTError:
            raise ValueError("Token expired or invalid")


auth_service = AuthService()
