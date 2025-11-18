import os
from pydantic_settings import BaseSettings
from pydantic import ConfigDict

class Settings(BaseSettings):
    api_url: str = ""
    secret_key: str = ""
    
    #model_config = ConfigDict(env_file=".env_conf")
    
    class Config:
        # Aqui definimos o arquivo .env padrão
        env_file = f".env.{os.getenv('APP_ENV', 'local')}"
        env_file_encoding = 'utf-8'
        
setting = Settings()