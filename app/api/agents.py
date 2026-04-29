"""
Agent orchestration API endpoints
"""
from fastapi import APIRouter, HTTPException, BackgroundTasks, Query
from typing import Optional
from pydantic import BaseModel
from enum import Enum
from datetime import datetime

router = APIRouter()


class AgentType(str, Enum):
    SCOUT = "scout"
    STRATEGIST = "strategist"
    GHOSTWRITER = "ghostwriter"
    LIAISON = "liaison"
    SENTINEL = "sentinel"


class AgentStatus(BaseModel):
    agent: AgentType
    status: str  # "idle", "running", "completed", "error"
    last_run: Optional[datetime] = None
    jobs_processed: int = 0
    message: Optional[str] = None


class RunAgentRequest(BaseModel):
    user_id: str
    job_ids: Optional[list[str]] = None  # For targeted runs


@router.get("/status")
async def get_all_agent_status(user_id: str = Query(...)):
    """
    Get status of all agents for a user.
    """
    # TODO: Fetch actual agent status from Supabase logs
    return {
        "success": True,
        "user_id": user_id,
        "agents": [
            {
                "agent": "scout",
                "status": "idle",
                "last_run": "2026-04-28T10:00:00Z",
                "jobs_processed": 47,
                "message": "Last scan: 47 new opportunities"
            },
            {
                "agent": "strategist",
                "status": "idle",
                "last_run": "2026-04-28T10:05:00Z",
                "jobs_processed": 47,
                "message": "Scored and ranked 47 jobs"
            },
            {
                "agent": "ghostwriter",
                "status": "idle",
                "last_run": "2026-04-28T09:30:00Z",
                "jobs_processed": 3,
                "message": "Prepared 3 applications"
            },
            {
                "agent": "liaison",
                "status": "idle",
                "last_run": "2026-04-28T09:35:00Z",
                "jobs_processed": 3,
                "message": "Submitted 3 applications"
            },
            {
                "agent": "sentinel",
                "status": "running",
                "last_run": "2026-04-28T10:10:00Z",
                "jobs_processed": 12,
                "message": "Monitoring inbox... 2 new recruiter emails detected"
            }
        ]
    }


@router.post("/run/{agent_type}")
async def run_agent(
    agent_type: AgentType,
    request: RunAgentRequest,
    background_tasks: BackgroundTasks
):
    """
    Manually trigger an agent run.
    """
    # TODO: Add actual agent execution to background tasks
    
    agent_descriptions = {
        AgentType.SCOUT: "Scanning job boards for new opportunities",
        AgentType.STRATEGIST: "Analyzing and scoring discovered jobs",
        AgentType.GHOSTWRITER: "Preparing tailored application materials",
        AgentType.LIAISON: "Submitting approved applications",
        AgentType.SENTINEL: "Monitoring email for recruiter responses"
    }
    
    return {
        "success": True,
        "agent": agent_type,
        "status": "started",
        "message": agent_descriptions.get(agent_type, "Agent started")
    }


@router.post("/run-pipeline")
async def run_full_pipeline(
    request: RunAgentRequest,
    background_tasks: BackgroundTasks
):
    """
    Run the full Sniper pipeline: Scout -> Strategist -> (await approval) -> Ghostwriter -> Liaison
    """
    # TODO: Implement full pipeline orchestration
    return {
        "success": True,
        "status": "pipeline_started",
        "message": "Full pipeline initiated. Scout is now searching for jobs.",
        "steps": [
            {"step": 1, "agent": "scout", "status": "running"},
            {"step": 2, "agent": "strategist", "status": "pending"},
            {"step": 3, "agent": "ghostwriter", "status": "pending"},
            {"step": 4, "agent": "liaison", "status": "pending"}
        ]
    }


@router.get("/logs")
async def get_agent_logs(
    user_id: str = Query(...),
    agent: Optional[AgentType] = Query(None),
    limit: int = Query(50)
):
    """
    Get agent activity logs.
    """
    # TODO: Fetch from Supabase agent_logs table
    return {
        "success": True,
        "logs": [
            {
                "id": "log_1",
                "agent": "scout",
                "action": "discover",
                "timestamp": "2026-04-28T10:00:00Z",
                "details": {"jobs_found": 47, "source": "adzuna"}
            },
            {
                "id": "log_2",
                "agent": "strategist",
                "action": "score",
                "timestamp": "2026-04-28T10:05:00Z",
                "details": {"jobs_scored": 47, "high_match": 12}
            },
            {
                "id": "log_3",
                "agent": "sentinel",
                "action": "email_detected",
                "timestamp": "2026-04-28T10:10:00Z",
                "details": {"type": "interview_invite", "company": "Stripe"}
            }
        ]
    }
