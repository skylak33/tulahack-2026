from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Path, status

from app.api.deps import get_manager
from app.repositories.team import team_repository
from app.repositories.user import user_repository
from app.schemas.team import AddMemberRequest, TeamCreate, TeamOut

router = APIRouter(prefix="/teams", tags=["teams"])

ManagerDep = Annotated[dict, Depends(get_manager)]


@router.get("/", response_model=list[TeamOut])
async def list_teams(current_user: ManagerDep) -> list[TeamOut]:
    return await team_repository.get_by_manager(current_user["id"])


@router.post("/", response_model=TeamOut, status_code=status.HTTP_201_CREATED)
async def create_team(data: TeamCreate, current_user: ManagerDep) -> TeamOut:
    return await team_repository.create(current_user["id"], data.name)


@router.get("/{team_id}", response_model=TeamOut)
async def get_team(
    team_id: Annotated[UUID, Path()],
    current_user: ManagerDep,
) -> TeamOut:
    team = await team_repository.get_by_id(team_id)
    if team is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Команда не найдена")
    if team["manager_id"] != current_user["id"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Нет доступа")
    return team


@router.delete("/{team_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_team(
    team_id: Annotated[UUID, Path()],
    current_user: ManagerDep,
) -> None:
    team = await team_repository.get_by_id(team_id)
    if team is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Команда не найдена")
    if team["manager_id"] != current_user["id"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Нет доступа")
    await team_repository.delete(team_id)


@router.post("/{team_id}/members", response_model=TeamOut)
async def add_member(
    team_id: Annotated[UUID, Path()],
    data: AddMemberRequest,
    current_user: ManagerDep,
) -> TeamOut:
    team = await team_repository.get_by_id(team_id)
    if team is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Команда не найдена")
    if team["manager_id"] != current_user["id"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Нет доступа")
    user = await user_repository.get_by_id(data.user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден")
    await team_repository.add_member(team_id, data.user_id)
    return await team_repository.get_by_id(team_id)


@router.delete("/{team_id}/members/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_member(
    team_id: Annotated[UUID, Path()],
    user_id: Annotated[UUID, Path()],
    current_user: ManagerDep,
) -> None:
    team = await team_repository.get_by_id(team_id)
    if team is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Команда не найдена")
    if team["manager_id"] != current_user["id"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Нет доступа")
    await team_repository.remove_member(team_id, user_id)
