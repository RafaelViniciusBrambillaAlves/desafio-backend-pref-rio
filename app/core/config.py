from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):

    DATABASE_URL: str
    DB_NAME: str

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    JWT_REFRESH_TOKEN_EXPIRES_MINUTES: int
    JWT_REFRESH_TOKEN_EXPIRES_DAYS: int

    model_config = SettingsConfigDict(
        env_file = ".env",
        extra = "forbid",
        case_sensitive = False
    )

settings = Settings()

