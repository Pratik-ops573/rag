from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Palm Mind RAG Backend"
    debug: bool = True

    qdrant_url: str
    qdrant_api_key: str

    openrouter_api_key: str
    openrouter_model: str = "openrouter/free"

    redis_url: str

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()