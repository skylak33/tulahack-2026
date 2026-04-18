from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database.db import database

from app.api.routers.auth import router as auth_router
from app.api.routers.users import router as users_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    yield
    await database.disconnect()

app = FastAPI(title="Team Builder API", lifespan=lifespan)

app.include_router(auth_router)
app.include_router(users_router)

@app.get("/health")
async def health_check():
    return {"status": "ok"}

# pip uninstall jwt pyjwt
# pip install pyjwt