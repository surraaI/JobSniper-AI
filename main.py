"""
JobSniper AI Backend - FastAPI Application
Multi-agent system for autonomous job hunting
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import health, jobs, profile, agents, telegram
from app.config import settings

app = FastAPI(
    title="JobSniper AI",
    description="Autonomous job hunting with AI agents",
    version="0.1.0",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, tags=["Health"])
app.include_router(profile.router, prefix="/profile", tags=["Profile"])
app.include_router(jobs.router, prefix="/jobs", tags=["Jobs"])
app.include_router(agents.router, prefix="/agents", tags=["Agents"])
app.include_router(telegram.router, prefix="/telegram", tags=["Telegram"])


@app.get("/")
async def root():
    return {
        "name": "JobSniper AI",
        "version": "0.1.0",
        "status": "operational",
        "agents": ["scout", "strategist", "ghostwriter", "liaison", "sentinel"],
    }
