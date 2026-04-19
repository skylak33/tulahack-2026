from fastapi import APIRouter, HTTPException, status
from datetime import timedelta
from app.schemas.user import UserCreate, UserFull, UserLogin, TokenPair, TokenRefresh
from app.services.auth import auth_service
from app.config import ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserFull, status_code=status.HTTP_201_CREATED)
async def register(user_in: UserCreate) -> UserFull:
    try:
        return await auth_service.register_user(user_in)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.post("/login", response_model=TokenPair)
async def login(user_in: UserLogin) -> TokenPair:
    user = await auth_service.authenticate_user(user_in.email, user_in.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверный email или пароль"
        )

    access_token = auth_service.create_token(
        data={"sub": str(user["id"]), "role": user["role"]},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    refresh_token = auth_service.create_token(
        data={"sub": str(user["id"])}, expires_delta=timedelta(days=7)
    )
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@router.post("/refresh", response_model=TokenPair)
async def refresh(refresh_data: TokenRefresh) -> TokenPair:
    try:
        new_access = auth_service.refresh_access_token(refresh_data.refresh_token)
        return {
            "access_token": new_access,
            "refresh_token": refresh_data.refresh_token,
            "token_type": "bearer",
        }
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
