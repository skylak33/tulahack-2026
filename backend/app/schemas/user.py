from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Dict, Any
from uuid import UUID
from datetime import datetime
from enum import Enum


class RoleEnum(str, Enum):
    manager = "manager"
    employee = "employee"
    candidate = "candidate"


class TeamRoleEnum(str, Enum):
    junior = "junior"
    middle = "middle"
    senior = "senior"
    lead = "lead"
    principal = "principal"


class DiscProfile(BaseModel):
    D: int = Field(ge=0, le=100)
    I: int = Field(ge=0, le=100)
    S: int = Field(ge=0, le=100)
    C: int = Field(ge=0, le=100)


class UserShort(BaseModel):
    id: UUID
    email: EmailStr
    full_name: str
    role: RoleEnum
    model_config = {"from_attributes": True}


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    full_name: str
    role: RoleEnum
    age: Optional[int] = None
    team_role: Optional[TeamRoleEnum] = None
    disc_profile: Optional[DiscProfile] = None
    motivation_profile: Optional[Dict[str, Any]] = None


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    age: Optional[int] = None
    team_role: Optional[TeamRoleEnum] = None
    disc_profile: Optional[DiscProfile] = None
    motivation_profile: Optional[Dict[str, Any]] = None


class UserFull(UserShort):
    age: Optional[int] = None
    team_role: Optional[TeamRoleEnum] = None
    disc_profile: Optional[DiscProfile] = None
    motivation_profile: Optional[Dict[str, Any]] = None
    created_at: datetime
    updated_at: datetime
    model_config = {"from_attributes": True}


class UserList(BaseModel):
    total: int
    items: list[UserShort]


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenRefresh(BaseModel):
    refresh_token: str
