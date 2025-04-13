from loguru import logger
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    A Pydantic-based settings class for managing application configurations.
    """


    # --- MongoDB Atlas Configuration ---
    MONGODB_DATABASE_NAME: str = Field(
        default="ai-newsletter",
        description="Name of the MongoDB database.",
    )
    MONGODB_URI: str = Field(
        default="mongodb://decodingml:decodingml@localhost:27017/?directConnection=true",
        description="Connection URI for the local MongoDB Atlas instance.",
    )
try:
    settings = Settings()
except Exception as e:
    logger.error(f"Failed to load configuration: {e}")
    raise SystemExit(e)
