from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database.db import database

from app.api.routers.auth import router as auth_router
from app.api.routers.search import router as search_router
from app.api.routers.teams import router as teams_router
from app.api.routers.users import router as users_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    yield
    await database.disconnect()

app = FastAPI(title="Team Builder API", lifespan=lifespan)

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(teams_router)
app.include_router(search_router)

@app.get("/health")
async def health_check():
    return {"status": "ok"}