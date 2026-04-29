"""
JobSniper AI Backend - Multi-Agent Job Hunting System
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import health, jobs, profile, agents, telegram

app = FastAPI(
    title="JobSniper AI",
    description="AI-powered job hunting with multi-agent orchestration",
    version="0.1.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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
        "agents": ["Scout", "Strategist", "Ghostwriter", "Liaison", "Sentinel"]
    }
