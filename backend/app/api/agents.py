"""Agents API endpoints - Orchestrate the AI agents"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

from app.services.supabase import get_client

router = APIRouter()


class HuntRequest(BaseModel):
    user_id: str
    query: Optional[str] = None
    location: Optional[str] = None
    limit: int = 20


class AnalyzeRequest(BaseModel):
    user_id: str
    job_ids: List[str]


class ApplyRequest(BaseModel):
    user_id: str
    job_id: str


@router.post("/scout/run")
async def run_scout_only(request: HuntRequest):
    """
    Run only the Scout agent to discover new jobs.
    """
    from app.agents.scout import ScoutAgent
    
    scout = ScoutAgent()
    
    try:
        # Get user profile for matching
        client = await get_client()
        profile_result = await client.table("profiles").select("*").eq("id", request.user_id).single().execute()
        profile = profile_result.data
        
        # Scout discovers jobs
        jobs = await scout.hunt(
            query=request.query or ", ".join(profile.get("preferences", {}).get("target_roles", [])),
            location=request.location,
            limit=request.limit,
        )
        
        # Log agent activity
        await client.table("agent_logs").insert({
            "user_id": request.user_id,
            "agent": "scout",
            "action": "hunt",
            "output_data": {"jobs_found": len(jobs)},
        }).execute()
        
        return {
            "success": True,
            "message": f"Scout found {len(jobs)} jobs matching your criteria",
            "data": {"jobs_found": len(jobs), "sample_jobs": jobs[:3]},
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/pipeline/run")
async def run_full_pipeline(request: HuntRequest):
    """
    Run the full pipeline: Scout + Strategist + store applications.
    """
    from app.agents.scout import ScoutAgent
    from app.agents.strategist import StrategistAgent
    
    scout = ScoutAgent()
    strategist = StrategistAgent()
    
    try:
        # Get user profile for matching
        client = await get_client()
        profile_result = await client.table("profiles").select("*").eq("id", request.user_id).single().execute()
        profile = profile_result.data
        
        # Scout discovers jobs
        jobs = await scout.hunt(
            query=request.query or ", ".join(profile.get("preferences", {}).get("target_roles", [])),
            location=request.location,
            limit=request.limit,
        )
        
        # Strategist scores each job
        scored_jobs = []
        for job in jobs:
            score = await strategist.score_match(job, profile)
            scored_jobs.append({**job, "match_score": score})
        
        # Sort by score
        scored_jobs.sort(key=lambda x: x.get("match_score", 0), reverse=True)
        
        # Store top matches as pending applications
        for job in scored_jobs[:10]:  # Top 10
            try:
                # Upsert job
                await client.table("jobs").upsert({
                    "external_id": job.get("external_id"),
                    "source": job.get("source", "adzuna"),
                    "company": job["company"],
                    "title": job["title"],
                    "description": job.get("description"),
                    "location": job.get("location"),
                    "salary_min": job.get("salary_min"),
                    "salary_max": job.get("salary_max"),
                    "job_url": job["job_url"],
                }).execute()
                
                # Get job ID
                job_result = await client.table("jobs").select("id").eq("external_id", job.get("external_id")).single().execute()
                
                # Create pending application
                await client.table("applications").upsert({
                    "user_id": request.user_id,
                    "job_id": job_result.data["id"],
                    "status": "pending_approval",
                    "match_score": job.get("match_score"),
                }).execute()
            except Exception:
                continue  # Skip duplicates
        
        # Log agent activity
        await client.table("agent_logs").insert({
            "user_id": request.user_id,
            "agent": "scout",
            "action": "full_pipeline",
            "output_data": {"jobs_found": len(jobs), "pending_approval": len(scored_jobs[:10])},
        }).execute()
        
        return {
            "success": True,
            "message": f"Pipeline complete! Found {len(jobs)} jobs, {len(scored_jobs[:10])} pending your approval",
            "data": {
                "jobs_found": len(jobs),
                "pending_approval": len(scored_jobs[:10]),
                "top_jobs": scored_jobs[:5],
            },
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/generate-application")
async def generate_application(request: ApplyRequest):
    """
    Generate tailored resume and cover letter for a job.
    Uses Ghostwriter agent.
    """
    from app.agents.ghostwriter import GhostwriterAgent
    
    ghostwriter = GhostwriterAgent()
    
    try:
        client = await get_client()
        
        # Get profile
        profile_result = await client.table("profiles").select("*").eq("id", request.user_id).single().execute()
        profile = profile_result.data
        
        # Get job
        job_result = await client.table("jobs").select("*").eq("id", request.job_id).single().execute()
        job = job_result.data
        
        # Generate application materials
        materials = await ghostwriter.craft_application(profile, job)
        
        # Update application with generated content
        await client.table("applications").update({
            "cover_letter": materials.get("cover_letter"),
            "tailored_resume": materials.get("tailored_resume"),
        }).eq("user_id", request.user_id).eq("job_id", request.job_id).execute()
        
        # Log activity
        await client.table("agent_logs").insert({
            "user_id": request.user_id,
            "agent": "ghostwriter",
            "action": "craft_application",
            "job_id": request.job_id,
        }).execute()
        
        return materials
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/generate-outreach")
async def generate_outreach(request: ApplyRequest):
    """
    Generate personalized outreach message for a recruiter.
    Uses Liaison agent.
    """
    from app.agents.liaison import LiaisonAgent
    
    liaison = LiaisonAgent()
    
    try:
        client = await get_client()
        
        # Get profile and job
        profile_result = await client.table("profiles").select("*").eq("id", request.user_id).single().execute()
        job_result = await client.table("jobs").select("*").eq("id", request.job_id).single().execute()
        
        message = await liaison.draft_outreach(profile_result.data, job_result.data)
        
        # Update application
        await client.table("applications").update({
            "outreach_message": message,
        }).eq("user_id", request.user_id).eq("job_id", request.job_id).execute()
        
        return {"outreach_message": message}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/check-emails")
async def check_emails(user_id: str):
    """
    Run Sentinel agent to check for interview invites and updates.
    """
    from app.agents.sentinel import SentinelAgent
    
    sentinel = SentinelAgent()
    
    try:
        updates = await sentinel.monitor(user_id)
        
        client = await get_client()
        await client.table("agent_logs").insert({
            "user_id": user_id,
            "agent": "sentinel",
            "action": "monitor_emails",
            "output_data": updates,
        }).execute()
        
        return updates
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/logs")
async def get_agent_logs(user_id: str, limit: int = 50):
    """Get recent agent activity logs"""
    try:
        client = await get_client()
        result = await client.table("agent_logs").select("*").eq("user_id", user_id).order("created_at", desc=True).limit(limit).execute()
        return {"logs": result.data}
    except Exception as e:
        return {"logs": []}
