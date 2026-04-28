"""
Configuration settings for JobSniper AI
"""
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # Supabase
    supabase_url: str = ""
    supabase_anon_key: str = ""
    supabase_service_role_key: str = ""
    
    # OpenAI
    openai_api_key: str = ""
    
    # Job APIs
    adzuna_app_id: str = ""
    adzuna_api_key: str = ""
    theirstack_api_key: str = ""
    
    # Telegram
    telegram_bot_token: str = ""
    
    # Gmail (OAuth2)
    gmail_client_id: str = ""
    gmail_client_secret: str = ""
    
    # App settings
    environment: str = "development"
    demo_mode: bool = True  # Fallback to demo data if APIs fail
    
    class Config:
        env_file = ".env"
        extra = "ignore"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
