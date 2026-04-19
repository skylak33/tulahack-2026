import uuid

from app.database.db import database
from app.database.models import teams, team_members, users


class TeamRepository:
    async def get_by_manager(self, manager_id: uuid.UUID) -> list[dict]:
        query = teams.select().where(teams.c.manager_id == manager_id)
        rows = await database.fetch_all(query)
        result = []
        for row in rows:
            members = await self._get_members(row["id"])
            result.append({**dict(row), "members": members})
        return result

    async def get_by_id(self, team_id: uuid.UUID) -> dict | None:
        query = teams.select().where(teams.c.id == team_id)
        row = await database.fetch_one(query)
        if row is None:
            return None
        members = await self._get_members(team_id)
        return {**dict(row), "members": members}

    async def create(self, manager_id: uuid.UUID, name: str) -> dict:
        team_id = uuid.uuid4()
        query = (
            teams.insert()
            .values(id=team_id, name=name, manager_id=manager_id)
            .returning(teams)
        )
        row = await database.fetch_one(query)
        return {**dict(row), "members": []}

    async def delete(self, team_id: uuid.UUID) -> None:
        query = teams.delete().where(teams.c.id == team_id)
        await database.execute(query)

    async def add_member(self, team_id: uuid.UUID, user_id: uuid.UUID) -> None:
        query = team_members.insert().values(team_id=team_id, user_id=user_id)
        await database.execute(query)

    async def remove_member(self, team_id: uuid.UUID, user_id: uuid.UUID) -> None:
        query = team_members.delete().where(
            (team_members.c.team_id == team_id) & (team_members.c.user_id == user_id)
        )
        await database.execute(query)

    async def is_owner(self, team_id: uuid.UUID, manager_id: uuid.UUID) -> bool:
        query = teams.select().where(
            (teams.c.id == team_id) & (teams.c.manager_id == manager_id)
        )
        return await database.fetch_one(query) is not None

    async def _get_members(self, team_id: uuid.UUID) -> list[dict]:
        query = (
            users.select()
            .join(team_members, users.c.id == team_members.c.user_id)
            .where(team_members.c.team_id == team_id)
        )
        rows = await database.fetch_all(query)
        return [dict(row) for row in rows]


team_repository = TeamRepository()
