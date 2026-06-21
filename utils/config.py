import os
from pydantic_settings import BaseSettings
from pydantic import Field, AliasChoices
from pydantic_settings import SettingsConfigDict

class Settings(BaseSettings):
    api_url: str = Field(..., min_length=1, validation_alias=AliasChoices("API_URL", "api_url"))
    secret_key: str = Field(..., min_length=1, validation_alias=AliasChoices("SECRET_KEY", "secret_key"))

    model_config = SettingsConfigDict(
        env_file=f".env.{os.getenv('APP_ENV', 'local')}",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

setting = Settings()
