from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_NAME: str = "AI Presentation Builder"
    ENV: str = "dev"
    API_PREFIX: str = "/api"
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    DB_URI: str  # postgres://user:pass@host:5432/db
    REDIS_URI: str  # redis://redis:6379/0

    S3_ENDPOINT: str
    S3_BUCKET: str
    S3_REGION: str | None = None
    S3_ACCESS_KEY: str
    S3_SECRET_KEY: str
    S3_SECURE: bool = True

    # Model provider (your choice)
    MODEL_BASE_URL: str | None = None
    MODEL_API_KEY: str | None = None

    CORS_ORIGINS: list[str] = []

    model_config = SettingsConfigDict(env_file='.env', case_sensitive=False)

settings = Settings()
