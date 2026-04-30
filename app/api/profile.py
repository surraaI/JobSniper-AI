"""Profile API endpoints"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List

from app.services.supabase import get_client

router = APIRouter()


class JobPreferences(BaseModel):
    target_roles: List[str] = []
    target_locations: List[str] = []
    remote_preference: str = "any"  # "remote", "hybrid", "onsite", "any"
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    company_size: List[str] = []  # "startup", "mid", "enterprise"
    industries: List[str] = []


class ProfileUpdate(BaseModel):
    full_name: Optional[str] = None
    linkedin_url: Optional[str] = None
    resume_text: Optional[str] = None
    skills: Optional[List[str]] = None
    experience_years: Optional[int] = None
    preferences: Optional[JobPreferences] = None


class TelegramConnect(BaseModel):
    telegram_chat_id: str


@router.get("/{user_id}")
async def get_profile(user_id: str):
    """Get user profile"""
    try:
        client = await get_client()
        result = await client.table("profiles").select("*").eq("id", user_id).single().execute()
        return result.data
    except Exception as e:
        raise HTTPException(status_code=404, detail="Profile not found")


@router.patch("/{user_id}")
async def update_profile(user_id: str, profile: ProfileUpdate):
    """Update user profile"""
    try:
        client = await get_client()
        
        update_data = profile.model_dump(exclude_none=True)
        if "preferences" in update_data:
            update_data["preferences"] = update_data["preferences"]
        
        result = await client.table("profiles").update(update_data).eq("id", user_id).execute()
        
        if not result.data:
            raise HTTPException(status_code=404, detail="Profile not found")
        
        return result.data[0]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{user_id}/connect-telegram")
async def connect_telegram(user_id: str, data: TelegramConnect):
    """Connect Telegram account to profile"""
    try:
        client = await get_client()
        
        result = await client.table("profiles").update({
            "telegram_chat_id": data.telegram_chat_id
        }).eq("id", user_id).execute()
        
        if not result.data:
            raise HTTPException(status_code=404, detail="Profile not found")
        
        return {"status": "connected", "telegram_chat_id": data.telegram_chat_id}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{user_id}/parse-resume")
async def parse_resume(user_id: str, resume_text: str):
    """Parse resume and extract skills using AI"""
    from app.services.openai import extract_resume_data
    
    try:
        extracted = await extract_resume_data(resume_text)
        
        # Update profile with extracted data
        client = await get_client()
        await client.table("profiles").update({
            "resume_text": resume_text,
            "skills": extracted.get("skills", []),
            "experience_years": extracted.get("experience_years"),
        }).eq("id", user_id).execute()
        
        return extracted
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
