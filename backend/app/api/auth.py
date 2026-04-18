from fastapi import APIRouter, HTTPException, status
from app.schemas.user import UserCreate, UserFull
from app.services.auth import auth_service

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserFull, status_code=status.HTTP_201_CREATED)
async def register(user_in: UserCreate):
    try:
        user = await auth_service.register_user(user_in)
        return user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )