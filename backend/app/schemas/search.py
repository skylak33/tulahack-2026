from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from app.schemas.user import UserFull


class SearchRequestCreate(BaseModel):
    query_text: str
    team_id: UUID


class CandidateResult(BaseModel):
    user: UserFull
    compatibility_score: float
    compatibility_summary: str
    strengths: list[str]
    risks: list[str]


class Verdict(BaseModel):
    candidates: list[CandidateResult]
    summary: str


class SearchRequestOut(BaseModel):
    id: UUID
    manager_id: UUID
    query_text: str
    verdict: Verdict | None = None
    created_at: datetime
    model_config = {"from_attributes": True}


class SearchList(BaseModel):
    total: int
    items: list[SearchRequestOut]
