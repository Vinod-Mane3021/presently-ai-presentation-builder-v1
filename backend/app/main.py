from fastapi import FastAPI
from app.settings import settings
from app.routers.user import router as user_router
from app.db import Base, engine

if settings.APP_ENV == "dev":
    print("⚙️  Creating tables (development mode only)...")
    Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.APP_NAME, version=settings.APP_VERSION)

app.include_router(user_router)

@app.get("/")
async def root():
    return {"message": "Server is up and running"}

