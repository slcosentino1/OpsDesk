from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    askdoc_base_url: str = "http://127.0.0.1:8000"
    llm_model: str = "llama3.2"
    llm_base_url: str = "http://localhost:11434/v1"
    llm_api_key: str = "ollama"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="OPSDESK_",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
