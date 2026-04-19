from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Path, Query, status

from app.api.deps import get_manager
from app.repositories.search import search_repository
from app.repositories.team import team_repository
from app.schemas.search import SearchList, SearchRequestCreate, SearchRequestOut
from app.services.search import analyze_candidates

router = APIRouter(prefix="/search", tags=["search"])

ManagerDep = Annotated[dict, Depends(get_manager)]


@router.post("/", response_model=SearchRequestOut, status_code=status.HTTP_201_CREATED)
async def create_search(
    data: SearchRequestCreate, current_user: ManagerDep
) -> SearchRequestOut:
    team = await team_repository.get_by_id(data.team_id)
    if team is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Команда не найдена"
        )
    if team["manager_id"] != current_user["id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Нет доступа к команде"
        )

    search = await search_repository.create(current_user["id"], data.query_text)

    candidates = await search_repository.get_all_candidates()
    verdict = await analyze_candidates(
        query_text=data.query_text,
        team_members=team["members"],
        candidates=candidates,
    )

    updated = await search_repository.update_verdict(search["id"], verdict)
    return updated


@router.get("/", response_model=SearchList)
async def list_searches(
    current_user: ManagerDep,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> SearchList:
    total, items = await search_repository.get_by_manager(
        current_user["id"], limit=limit, offset=offset
    )
    return SearchList(total=total, items=items)


@router.get("/{search_id}", response_model=SearchRequestOut)
async def get_search(
    search_id: Annotated[UUID, Path()],
    current_user: ManagerDep,
) -> SearchRequestOut:
    search = await search_repository.get_by_id(search_id)
    if search is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Запрос не найден"
        )
    if search["manager_id"] != current_user["id"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Нет доступа")
    return search
