from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Path, Query, status

from app.api.deps import get_current_user, get_manager
from app.repositories.user import user_repository
from app.schemas.user import RoleEnum, TeamRoleEnum, UserCreate, UserFull, UserList, UserUpdate
from app.services.auth import auth_service

router = APIRouter(prefix="/users", tags=["users"])

CurrentUserDep = Annotated[dict, Depends(get_current_user)]
ManagerDep = Annotated[dict, Depends(get_manager)]

@router.get("/me", response_model=UserFull)
async def get_me(current_user: CurrentUserDep) -> UserFull:
    return current_user


@router.patch("/me", response_model=UserFull)
async def update_me(data: UserUpdate, current_user: CurrentUserDep) -> UserFull:
    update_data = data.model_dump(exclude_unset=True)
    if not update_data:
        return current_user
    return await user_repository.update(current_user["id"], update_data)


@router.get("/", response_model=UserList)
async def list_users(
        current_user: ManagerDep,
        role: Annotated[RoleEnum | None, Query()] = None,
        team_role: Annotated[TeamRoleEnum | None, Query()] = None,
        limit: Annotated[int, Query(ge=1, le=200)] = 50,
        offset: Annotated[int, Query(ge=0)] = 0,
) -> UserList:
    total, items = await user_repository.get_all(
        role=role, team_role=team_role, limit=limit, offset=offset
    )
    return UserList(total=total, items=items)


@router.post("/", response_model=UserFull, status_code=status.HTTP_201_CREATED)
async def create_user(data: UserCreate, current_user: ManagerDep) -> UserFull:
    try:
        return await auth_service.register_user(data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.get("/{user_id}", response_model=UserFull)
async def get_user(
        user_id: Annotated[UUID, Path()],
        current_user: ManagerDep,
) -> UserFull:
    user = await user_repository.get_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден")
    return user


@router.patch("/{user_id}", response_model=UserFull)
async def update_user(
        user_id: Annotated[UUID, Path()],
        data: UserUpdate,
        current_user: ManagerDep,
) -> UserFull:
    user = await user_repository.get_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден")
    update_data = data.model_dump(exclude_unset=True)
    if not update_data:
        return user
    return await user_repository.update(user_id, update_data)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
        user_id: Annotated[UUID, Path()],
        current_user: ManagerDep,
) -> None:
    user = await user_repository.get_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден")
    await user_repository.delete(user_id)
