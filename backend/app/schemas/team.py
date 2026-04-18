from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

from app.schemas.user import UserShort


class TeamCreate(BaseModel):
    name: str


class AddMemberRequest(BaseModel):
    user_id: UUID


class TeamOut(BaseModel):
    id: UUID
    name: str
    manager_id: UUID
    members: list[UserShort]
    created_at: datetime
    model_config = {"from_attributes": True}
