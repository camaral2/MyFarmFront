from pydantic_settings import BaseSettings
from pydantic import ConfigDict

class Settings(BaseSettings):
    api_url: str = ""
    secret_key: str = ""
    
    model_config = ConfigDict(env_file=".env_conf")
    
setting = Settings()