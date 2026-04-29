"""
Supabase client for the backend
"""
import os
from supabase import create_client, Client
from typing import Optional

_supabase_client: Optional[Client] = None


def get_supabase() -> Client:
    """Get or create Supabase client singleton"""
    global _supabase_client
    
    if _supabase_client is None:
        url = os.environ.get("SUPABASE_URL")
        key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
        
        if not url or not key:
            raise ValueError("SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY must be set")
        
        _supabase_client = create_client(url, key)
    
    return _supabase_client


async def get_user_profile(user_id: str) -> dict | None:
    """Get user profile by ID"""
    supabase = get_supabase()
    result = supabase.table("profiles").select("*").eq("id", user_id).single().execute()
    return result.data if result.data else None


async def update_user_profile(user_id: str, data: dict) -> dict | None:
    """Update user profile"""
    supabase = get_supabase()
    result = supabase.table("profiles").update(data).eq("id", user_id).execute()
    return result.data[0] if result.data else None


async def get_jobs(limit: int = 50, offset: int = 0) -> list[dict]:
    """Get jobs from database"""
    supabase = get_supabase()
    result = supabase.table("jobs").select("*").order("posted_at", desc=True).range(offset, offset + limit - 1).execute()
    return result.data or []


async def upsert_jobs(jobs: list[dict]) -> list[dict]:
    """Upsert jobs into database"""
    supabase = get_supabase()
    result = supabase.table("jobs").upsert(jobs, on_conflict="external_id,source").execute()
    return result.data or []


async def get_user_applications(user_id: str) -> list[dict]:
    """Get all applications for a user with job details"""
    supabase = get_supabase()
    result = supabase.table("applications").select("*, jobs(*)").eq("user_id", user_id).order("created_at", desc=True).execute()
    return result.data or []


async def create_application(user_id: str, job_id: str, match_score: int) -> dict | None:
    """Create a new application"""
    supabase = get_supabase()
    result = supabase.table("applications").insert({
        "user_id": user_id,
        "job_id": job_id,
        "match_score": match_score,
        "status": "pending_approval"
    }).execute()
    return result.data[0] if result.data else None


async def update_application(application_id: str, data: dict) -> dict | None:
    """Update an application"""
    supabase = get_supabase()
    result = supabase.table("applications").update(data).eq("id", application_id).execute()
    return result.data[0] if result.data else None


async def log_agent_activity(
    user_id: str | None,
    agent: str,
    action: str,
    job_id: str | None = None,
    application_id: str | None = None,
    input_data: dict | None = None,
    output_data: dict | None = None,
    error: str | None = None,
    duration_ms: int | None = None
) -> dict | None:
    """Log agent activity"""
    supabase = get_supabase()
    result = supabase.table("agent_logs").insert({
        "user_id": user_id,
        "agent": agent,
        "action": action,
        "job_id": job_id,
        "application_id": application_id,
        "input_data": input_data,
        "output_data": output_data,
        "error": error,
        "duration_ms": duration_ms
    }).execute()
    return result.data[0] if result.data else None
