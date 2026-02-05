from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):

    DATABASE_URL: str
    DB_NAME: str

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    JWT_REFRESH_TOKEN_EXPIRES_MINUTES: int
    JWT_REFRESH_TOKEN_EXPIRES_DAYS: int

    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    GOOGLE_REDIRECT_URI: str

    MINIO_ENDPOINT: str
    MINIO_ACCESS_KEY: str 
    MINIO_SECRET_KEY: str
    MINIO_BUCKET: str
    MINIO_SECURE: bool = False

    model_config = SettingsConfigDict(
        env_file = ".env",
        extra = "forbid",
        case_sensitive = False
    )

settings = Settings()
