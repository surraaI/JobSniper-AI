"""
Jobs API endpoints
"""
from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from pydantic import BaseModel
from datetime import datetime
from enum import Enum

from app.agents.scout import ScoutAgent
from app.services.demo_data import get_demo_jobs

router = APIRouter()


class JobStatus(str, Enum):
    DISCOVERED = "discovered"
    PENDING_APPROVAL = "pending_approval"
    APPROVED = "approved"
    APPLIED = "applied"
    UNDER_REVIEW = "under_review"
    ASSESSMENT = "assessment"
    INTERVIEW_SCHEDULED = "interview_scheduled"
    INTERVIEW = "interview"
    OFFER = "offer"
    REJECTED = "rejected"


class Job(BaseModel):
    id: str
    company: str
    position: str
    location: str
    salary: Optional[str] = None
    description: Optional[str] = None
    url: str
    source: str  # adzuna, theirstack, linkedin, upwork
    match_score: Optional[int] = None
    status: JobStatus = JobStatus.DISCOVERED
    discovered_at: datetime
    applied_at: Optional[datetime] = None
    sentinel_update: Optional[str] = None
    deadline: Optional[datetime] = None


class JobSearchParams(BaseModel):
    keywords: str
    location: Optional[str] = None
    remote: bool = True
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None


@router.get("/discover")
async def discover_jobs(
    keywords: str = Query(..., description="Job search keywords"),
    location: Optional[str] = Query(None, description="Location filter"),
    remote: bool = Query(True, description="Include remote jobs"),
    limit: int = Query(20, description="Max results")
):
    """
    Trigger the Scout agent to discover new job opportunities.
    Falls back to demo data if external APIs fail.
    """
    scout = ScoutAgent()
    
    try:
        jobs = await scout.discover(
            keywords=keywords,
            location=location,
            remote=remote,
            limit=limit
        )
        return {
            "success": True,
            "source": "live",
            "count": len(jobs),
            "jobs": jobs
        }
    except Exception as e:
        # Fallback to demo data
        demo_jobs = get_demo_jobs(keywords=keywords, limit=limit)
        return {
            "success": True,
            "source": "demo",
            "fallback_reason": str(e),
            "count": len(demo_jobs),
            "jobs": demo_jobs
        }


@router.get("/applications")
async def get_applications(
    user_id: str = Query(..., description="User ID"),
    status: Optional[JobStatus] = Query(None, description="Filter by status")
):
    """
    Get all job applications for a user.
    """
    # TODO: Fetch from Supabase
    demo_jobs = get_demo_jobs(limit=10)
    
    if status:
        demo_jobs = [j for j in demo_jobs if j.get("status") == status]
    
    return {
        "success": True,
        "count": len(demo_jobs),
        "applications": demo_jobs
    }


@router.post("/approve/{job_id}")
async def approve_job(job_id: str, user_id: str = Query(...)):
    """
    Approve a job for application (human-in-the-loop).
    This triggers the Ghostwriter agent to prepare application materials.
    """
    # TODO: Update in Supabase, trigger Ghostwriter
    return {
        "success": True,
        "job_id": job_id,
        "status": "approved",
        "message": "Job approved. Ghostwriter is preparing your application."
    }


@router.post("/reject/{job_id}")
async def reject_job(job_id: str, user_id: str = Query(...)):
    """
    Reject a discovered job (don't apply).
    """
    # TODO: Update in Supabase
    return {
        "success": True,
        "job_id": job_id,
        "status": "rejected",
        "message": "Job removed from queue."
    }
