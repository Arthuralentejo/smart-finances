from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime settings loaded from environment variables."""

    model_config = SettingsConfigDict(extra="ignore")
    llm_model: str = "gpt-4o"
    ocr_service_base_url: str = "http://paddle-ocr:8001"
    ocr_service_timeout: int = 60
    tavily_api_key: str | None = None


settings = Settings()
