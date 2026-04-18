import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import ValidationError

from app.config import SECRET_KEY, ALGORITHM
from app.repositories.user import user_repository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Не удалось валидировать учетные данные",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except (jwt.PyJWTError, ValidationError):
        raise credentials_exception

    user = await user_repository.get_by_id(user_id)
    if user is None:
        raise credentials_exception

    return user


async def get_manager(current_user=Depends(get_current_user)):
    if current_user["role"] != "manager":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Недостаточно прав (нужна роль manager)"
        )
    return current_user