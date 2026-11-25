from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "Siyantech Gym OS"
    ENVIRONMENT: str = "development"
    SECRET_KEY: str = "dev_secret_key_change_in_production_min_32_chars_12345"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 hours
    
    # Databases
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres_dev_password@localhost:5432/siyantech_gym_os"
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # WhatsApp (Optional in Sprint 1)
    WHATSAPP_TOKEN: Optional[str] = None
    WHATSAPP_PHONE_NUMBER_ID: Optional[str] = None

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
