from pydantic import BaseSettings, ConfigDict


class Settings(BaseSettings):
    """Runtime settings loaded from environment variables."""

    model_config = ConfigDict(extra="ignore")
    ocr_service_url: str = "http://paddle-ocr:8001/ocr"


settings = Settings()
