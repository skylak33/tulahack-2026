import uuid
from datetime import datetime

import sqlalchemy as sa

from app.database.db import database
from app.database.models import search_requests, users


class SearchRepository:
    async def create(self, manager_id: uuid.UUID, query_text: str) -> dict:
        query = (
            search_requests.insert()
            .values(id=uuid.uuid4(), manager_id=manager_id, query_text=query_text)
            .returning(search_requests)
        )
        return dict(await database.fetch_one(query))

    async def update_verdict(self, search_id: uuid.UUID, verdict: dict) -> dict:
        query = (
            search_requests.update()
            .where(search_requests.c.id == search_id)
            .values(verdict=verdict)
            .returning(search_requests)
        )
        return dict(await database.fetch_one(query))

    async def get_by_id(self, search_id: uuid.UUID) -> dict | None:
        query = search_requests.select().where(search_requests.c.id == search_id)
        row = await database.fetch_one(query)
        return dict(row) if row else None

    async def get_by_manager(
        self, manager_id: uuid.UUID, limit: int = 20, offset: int = 0
    ) -> tuple[int, list[dict]]:
        base = search_requests.select().where(
            search_requests.c.manager_id == manager_id
        )
        count_base = (
            sa.select(sa.func.count())
            .select_from(search_requests)
            .where(search_requests.c.manager_id == manager_id)
        )
        total = await database.fetch_val(count_base)
        items = await database.fetch_all(
            base.order_by(search_requests.c.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        return total, [dict(r) for r in items]

    async def get_all_candidates(self) -> list[dict]:
        query = users.select().where(users.c.role == "candidate")
        rows = await database.fetch_all(query)
        return [dict(r) for r in rows]


search_repository = SearchRepository()
