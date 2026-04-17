import uuid
from sqlalchemy import Table, Column, String, Integer, DateTime, Enum, JSON, ForeignKey, Text, func
from sqlalchemy.dialects.postgresql import UUID

from app.database.db import metadata

RoleEnum = Enum("manager", "employee", "candidate", name="role_enum")
TeamRoleEnum = Enum("junior", "middle", "senior", "lead", "principal", name="team_role_enum")

users = Table(
    "users",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column("email", String, unique=True, index=True, nullable=False),
    Column("hashed_password", String, nullable=False),
    Column("role", RoleEnum, nullable=False),

    Column("full_name", String, nullable=False),
    Column("age", Integer, nullable=True),
    Column("team_role", TeamRoleEnum, nullable=True),

    Column("disc_profile", JSON, nullable=True),
    Column("motivation_profile", JSON, nullable=True),

    Column("created_at", DateTime(timezone=True), server_default=func.now()),
    Column("updated_at", DateTime(timezone=True), server_default=func.now(), onupdate=func.now()),
)

teams = Table(
    "teams",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column("name", String, nullable=False),
    Column("manager_id", UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
    Column("created_at", DateTime(timezone=True), server_default=func.now()),
)

team_members = Table(
    "team_members",
    metadata,
    Column("team_id", UUID(as_uuid=True), ForeignKey("teams.id", ondelete="CASCADE"), primary_key=True),
    Column("user_id", UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
)

search_requests = Table(
    "search_requests",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column("manager_id", UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
    Column("query_text", Text, nullable=False),
    Column("verdict", JSON, nullable=True),
    Column("created_at", DateTime(timezone=True), server_default=func.now()),
)