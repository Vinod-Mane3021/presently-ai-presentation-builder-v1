from fastapi import FastAPI
from app.settings import settings
from app.routers.user import router as user_router
from app.routers.content_generation import router as content_generation_router
from app.db import Base, engine
from logging.config import dictConfig
from app.config.logging_conf import LOGGING_CONFIG

dictConfig(LOGGING_CONFIG)

# if settings.APP_ENV == "dev":
#     print("⚙️  Creating tables (development mode only)...")
#     Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.APP_NAME, version=settings.APP_VERSION)

app.include_router(user_router)
app.include_router(content_generation_router)

@app.get("/")
async def root():
    return {"message": "Server is up and running"}






