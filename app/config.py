from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str
    TOKEN_EXPIRY_DAYS: int
    TOKEN_STORAGE: str

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
