"""
Configuration settings for JobSniper AI Backend
"""

from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    # Supabase
    supabase_url: str = os.getenv("SUPABASE_URL", "")
    supabase_key: str = os.getenv("SUPABASE_ANON_KEY", "")
    supabase_service_key: str = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")
    
    # OpenAI
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    
    # Telegram
    telegram_bot_token: str = os.getenv("TELEGRAM_BOT_TOKEN", "")
    
    # Job APIs
    adzuna_app_id: str = os.getenv("ADZUNA_APP_ID", "")
    adzuna_api_key: str = os.getenv("ADZUNA_API_KEY", "")
    theirstack_api_key: str = os.getenv("THEIRSTACK_API_KEY", "")
    
    # CORS
    cors_origins: List[str] = ["*"]
    
    # Demo mode (fallback when APIs unavailable)
    demo_mode: bool = os.getenv("DEMO_MODE", "true").lower() == "true"
    
    class Config:
        env_file = ".env"


settings = Settings()
