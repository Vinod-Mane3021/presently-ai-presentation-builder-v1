from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_ENV: str

    APP_NAME: str
    APP_VERSION: str
    DATABASE_URL: str
    PASSWORD_HASH_SECRET_KEY: str

    model_config = SettingsConfigDict(env_file='.env', case_sensitive=False)

settings = Settings()
