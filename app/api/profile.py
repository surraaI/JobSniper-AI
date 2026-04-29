"""
Profile API endpoints
"""
from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from typing import Optional, List
from pydantic import BaseModel

router = APIRouter()


class JobPreferences(BaseModel):
    target_roles: List[str]
    target_locations: List[str]
    remote_preference: str  # "remote_only", "hybrid", "onsite", "any"
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    company_size: List[str] = []  # "startup", "mid", "enterprise"
    industries: List[str] = []


class UserProfile(BaseModel):
    user_id: str
    full_name: str
    email: str
    linkedin_url: Optional[str] = None
    resume_text: Optional[str] = None
    skills: List[str] = []
    experience_years: Optional[int] = None
    preferences: Optional[JobPreferences] = None
    telegram_chat_id: Optional[str] = None


@router.get("/{user_id}")
async def get_profile(user_id: str):
    """
    Get user profile including preferences.
    """
    # TODO: Fetch from Supabase
    return {
        "success": True,
        "profile": {
            "user_id": user_id,
            "full_name": "Demo User",
            "email": "demo@jobsniper.ai",
            "skills": ["Python", "JavaScript", "React", "FastAPI"],
            "experience_years": 5,
            "preferences": {
                "target_roles": ["Full Stack Engineer", "Backend Engineer"],
                "target_locations": ["Remote", "San Francisco"],
                "remote_preference": "remote_only",
                "salary_min": 150000,
                "salary_max": 250000
            }
        }
    }


@router.post("/")
async def create_or_update_profile(profile: UserProfile):
    """
    Create or update user profile.
    """
    # TODO: Upsert to Supabase
    return {
        "success": True,
        "message": "Profile saved successfully",
        "profile": profile
    }


@router.post("/{user_id}/resume")
async def upload_resume(
    user_id: str,
    file: UploadFile = File(...)
):
    """
    Upload and parse resume (PDF/DOCX).
    """
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")
    
    # Check file type
    allowed_types = [".pdf", ".docx", ".doc", ".txt"]
    ext = "." + file.filename.split(".")[-1].lower()
    if ext not in allowed_types:
        raise HTTPException(
            status_code=400, 
            detail=f"File type not allowed. Use: {allowed_types}"
        )
    
    # TODO: Parse resume, extract skills, experience
    # TODO: Store in Supabase
    
    return {
        "success": True,
        "message": "Resume uploaded and parsed",
        "extracted": {
            "skills": ["Python", "JavaScript", "SQL", "AWS"],
            "experience_years": 5,
            "education": "BS Computer Science"
        }
    }


@router.post("/{user_id}/linkedin")
async def import_linkedin(
    user_id: str,
    linkedin_url: str = Form(...)
):
    """
    Import profile from LinkedIn URL.
    Uses Crawl4AI for extraction.
    """
    # TODO: Use Crawl4AI to extract LinkedIn profile
    return {
        "success": True,
        "message": "LinkedIn profile imported",
        "profile": {
            "name": "Demo User",
            "headline": "Full Stack Engineer",
            "location": "San Francisco Bay Area",
            "skills": ["Python", "React", "Node.js", "PostgreSQL"]
        }
    }


@router.put("/{user_id}/preferences")
async def update_preferences(user_id: str, preferences: JobPreferences):
    """
    Update job search preferences.
    """
    # TODO: Update in Supabase
    return {
        "success": True,
        "message": "Preferences updated",
        "preferences": preferences
    }
