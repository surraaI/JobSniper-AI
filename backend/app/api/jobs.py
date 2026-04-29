"""Jobs API endpoints"""

from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime

from app.services.supabase import get_client
from app.services.demo_data import get_demo_jobs
from app.config import settings

router = APIRouter()


class Job(BaseModel):
    id: str
    external_id: Optional[str] = None
    source: str = "adzuna"
    company: str
    title: str
    description: Optional[str] = None
    location: Optional[str] = None
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    job_url: str
    posted_at: Optional[datetime] = None
    requirements: Optional[List[str]] = None
    job_type: Optional[str] = None
    remote_type: Optional[str] = None


class Application(BaseModel):
    id: str
    job_id: str
    status: str
    match_score: Optional[int] = None
    sentinel_update: Optional[str] = None
    deadline: Optional[datetime] = None
    applied_at: Optional[datetime] = None
    job: Optional[Job] = None


@router.get("/discover")
async def discover_jobs(
    query: Optional[str] = Query(None, description="Search query"),
    location: Optional[str] = Query(None, description="Location filter"),
    remote: Optional[bool] = Query(None, description="Remote only"),
    limit: int = Query(20, le=100),
):
    """Discover new jobs using Scout agent"""
    from app.agents.scout import ScoutAgent
    
    scout = ScoutAgent()
    try:
        jobs = await scout.hunt(
            query=query,
            location=location,
            remote_only=remote,
            limit=limit,
        )
        return {"jobs": jobs, "count": len(jobs), "source": "live" if not settings.demo_mode else "demo"}
    except Exception as e:
        # Fallback to demo data
        demo_jobs = get_demo_jobs(limit=limit)
        return {"jobs": demo_jobs, "count": len(demo_jobs), "source": "demo", "error": str(e)}


@router.get("/applications")
async def get_applications(
    user_id: str,
    status: Optional[str] = Query(None),
):
    """Get user's job applications"""
    try:
        client = await get_client()
        query = client.table("applications").select("*, jobs(*)").eq("user_id", user_id)
        
        if status:
            query = query.eq("status", status)
        
        result = await query.order("created_at", desc=True).execute()
        return {"applications": result.data}
    except Exception as e:
        # Fallback to demo data
        from app.services.demo_data import get_demo_applications
        return {"applications": get_demo_applications(), "source": "demo"}


@router.post("/applications/{job_id}/approve")
async def approve_application(job_id: str, user_id: str):
    """Approve a job application for submission"""
    try:
        client = await get_client()
        
        # Update application status
        result = await client.table("applications").update({
            "status": "approved",
            "approved_at": datetime.utcnow().isoformat(),
        }).eq("job_id", job_id).eq("user_id", user_id).execute()
        
        if not result.data:
            raise HTTPException(status_code=404, detail="Application not found")
        
        return {"status": "approved", "application": result.data[0]}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/applications/{job_id}/reject")
async def reject_application(job_id: str, user_id: str):
    """Reject a job application"""
    try:
        client = await get_client()
        
        result = await client.table("applications").update({
            "status": "withdrawn",
        }).eq("job_id", job_id).eq("user_id", user_id).execute()
        
        return {"status": "withdrawn", "application": result.data[0] if result.data else None}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stats")
async def get_job_stats(user_id: str):
    """Get job application statistics"""
    try:
        client = await get_client()
        result = await client.table("applications").select("status").eq("user_id", user_id).execute()
        
        stats = {
            "total": len(result.data),
            "applied": 0,
            "interviews": 0,
            "offers": 0,
            "rejected": 0,
            "pending": 0,
        }
        
        for app in result.data:
            status = app["status"]
            if status in ["applied", "under_review"]:
                stats["applied"] += 1
            elif status in ["interview", "interview_scheduled", "assessment"]:
                stats["interviews"] += 1
            elif status == "offer":
                stats["offers"] += 1
            elif status == "rejected":
                stats["rejected"] += 1
            elif status in ["pending_approval", "approved"]:
                stats["pending"] += 1
        
        return stats
    except Exception as e:
        return {"total": 0, "applied": 0, "interviews": 0, "offers": 0, "rejected": 0, "pending": 0}
