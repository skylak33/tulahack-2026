from fastapi import APIRouter, Depends
from app.schemas.user import UserFull
from app.api.deps import get_current_user

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me", response_model=UserFull)
async def read_users_me(current_user = Depends(get_current_user)):
    return current_user