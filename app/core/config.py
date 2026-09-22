from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name:str="palm mind backend"
    debug:bool =True
    qdrant_api_key: str
    qdrant_url: str


    model_config=SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

settings=Settings()