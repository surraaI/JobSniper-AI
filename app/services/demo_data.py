"""
Demo Data Service - Fallback data for hackathon safety
Provides realistic job data when external APIs are unavailable.
"""
from datetime import datetime, timedelta
from typing import Optional
import random


# Pre-populated demo jobs for instant fallback
DEMO_JOBS = [
    {
        "id": "demo_stripe_1",
        "company": "Stripe",
        "position": "Senior Frontend Engineer",
        "location": "San Francisco, CA (Remote)",
        "salary": "$180,000 - $220,000",
        "description": "Join Stripe's Dashboard team to build the future of online payments. You'll work on React-based interfaces used by millions of businesses worldwide. Strong TypeScript skills required.",
        "url": "https://stripe.com/jobs",
        "source": "demo",
        "discovered_at": (datetime.utcnow() - timedelta(hours=2)).isoformat(),
        "status": "discovered",
        "match_score": 94
    },
    {
        "id": "demo_vercel_1",
        "company": "Vercel",
        "position": "Staff Software Engineer",
        "location": "Remote",
        "salary": "$200,000 - $250,000",
        "description": "Help build the future of web development at Vercel. Work on Next.js, Edge Functions, and developer tools. Looking for engineers passionate about DX.",
        "url": "https://vercel.com/careers",
        "source": "demo",
        "discovered_at": (datetime.utcnow() - timedelta(hours=4)).isoformat(),
        "status": "discovered",
        "match_score": 91
    },
    {
        "id": "demo_linear_1",
        "company": "Linear",
        "position": "Full Stack Developer",
        "location": "Remote (US/EU)",
        "salary": "$150,000 - $190,000",
        "description": "Build beautiful, performant software at Linear. We're creating the best issue tracking tool for modern software teams. React, TypeScript, GraphQL experience preferred.",
        "url": "https://linear.app/careers",
        "source": "demo",
        "discovered_at": (datetime.utcnow() - timedelta(hours=6)).isoformat(),
        "status": "discovered",
        "match_score": 88
    },
    {
        "id": "demo_notion_1",
        "company": "Notion",
        "position": "Product Engineer",
        "location": "New York, NY (Hybrid)",
        "salary": "$170,000 - $210,000",
        "description": "Shape the future of productivity tools at Notion. You'll work across the full stack building features that millions of users love. React, Node.js, PostgreSQL.",
        "url": "https://notion.so/careers",
        "source": "demo",
        "discovered_at": (datetime.utcnow() - timedelta(hours=8)).isoformat(),
        "status": "discovered",
        "match_score": 86
    },
    {
        "id": "demo_anthropic_1",
        "company": "Anthropic",
        "position": "ML Engineer",
        "location": "San Francisco, CA",
        "salary": "$250,000 - $350,000",
        "description": "Work on cutting-edge AI safety research at Anthropic. Help build Claude and advance the field of beneficial AI. Strong ML/Python background required.",
        "url": "https://anthropic.com/careers",
        "source": "demo",
        "discovered_at": (datetime.utcnow() - timedelta(hours=10)).isoformat(),
        "status": "discovered",
        "match_score": 79
    },
    {
        "id": "demo_figma_1",
        "company": "Figma",
        "position": "Senior Software Engineer",
        "location": "San Francisco, CA",
        "salary": "$175,000 - $225,000",
        "description": "Build the collaborative design tool used by designers worldwide. Work on real-time collaboration, WebGL rendering, and performance optimization.",
        "url": "https://figma.com/careers",
        "source": "demo",
        "discovered_at": (datetime.utcnow() - timedelta(hours=12)).isoformat(),
        "status": "discovered",
        "match_score": 82
    },
    {
        "id": "demo_bending_1",
        "company": "Bending Spoons",
        "position": "Product Intern - Evernote",
        "location": "Milan, Italy (Remote)",
        "salary": "€40,000 - €50,000",
        "description": "Join the team behind Evernote and other popular apps. Work on product development and help shape features used by millions. Great learning opportunity.",
        "url": "https://bendingspoons.com/careers",
        "source": "demo",
        "discovered_at": (datetime.utcnow() - timedelta(hours=14)).isoformat(),
        "status": "discovered",
        "match_score": 85
    },
    {
        "id": "demo_plaid_1",
        "company": "Plaid",
        "position": "Software Engineer",
        "location": "Remote",
        "salary": "$160,000 - $200,000",
        "description": "Build the infrastructure that powers fintech. Work on APIs connecting thousands of financial institutions. Python, Go, or Java experience required.",
        "url": "https://plaid.com/careers",
        "source": "demo",
        "discovered_at": (datetime.utcnow() - timedelta(hours=16)).isoformat(),
        "status": "discovered",
        "match_score": 83
    },
    {
        "id": "demo_datadog_1",
        "company": "Datadog",
        "position": "Frontend Engineer",
        "location": "Boston, MA (Hybrid)",
        "salary": "$140,000 - $180,000",
        "description": "Build dashboards and visualizations for the leading observability platform. React, TypeScript, data visualization experience preferred.",
        "url": "https://datadog.com/careers",
        "source": "demo",
        "discovered_at": (datetime.utcnow() - timedelta(hours=18)).isoformat(),
        "status": "discovered",
        "match_score": 85
    },
    {
        "id": "demo_openai_1",
        "company": "OpenAI",
        "position": "Research Engineer",
        "location": "San Francisco, CA",
        "salary": "$300,000 - $400,000",
        "description": "Push the boundaries of AI research. Work on large language models, safety, and deployment. PhD or equivalent experience in ML required.",
        "url": "https://openai.com/careers",
        "source": "demo",
        "discovered_at": (datetime.utcnow() - timedelta(hours=20)).isoformat(),
        "status": "discovered",
        "match_score": 75
    }
]


def get_demo_jobs(
    keywords: Optional[str] = None,
    location: Optional[str] = None,
    limit: int = 20
) -> list[dict]:
    """
    Get demo jobs, optionally filtered by keywords.
    """
    jobs = DEMO_JOBS.copy()
    
    if keywords:
        keywords_lower = keywords.lower()
        jobs = [
            j for j in jobs
            if keywords_lower in j["position"].lower()
            or keywords_lower in j["description"].lower()
            or keywords_lower in j["company"].lower()
        ]
    
    if location:
        location_lower = location.lower()
        jobs = [
            j for j in jobs
            if location_lower in j["location"].lower()
            or "remote" in j["location"].lower()
        ]
    
    # Randomize order slightly for variety
    random.shuffle(jobs)
    
    return jobs[:limit]


def get_demo_applications(user_id: str, limit: int = 10) -> list[dict]:
    """
    Get demo applications with various statuses.
    """
    statuses = [
        ("applied", None, None),
        ("under_review", "Application viewed by recruiter", None),
        ("assessment", "Technical assessment received - BRGHT IQ Test", "2026-05-01"),
        ("interview_scheduled", "Calendly link detected - Interview confirmed", None),
        ("interview", "Completed first round, awaiting feedback", None),
        ("offer", "Offer letter detected in inbox", None),
        ("rejected", "Rejection email detected - 2 similar roles found", None),
    ]
    
    applications = []
    for i, job in enumerate(DEMO_JOBS[:limit]):
        status, sentinel_update, deadline = statuses[i % len(statuses)]
        app = job.copy()
        app["status"] = status
        app["applied_at"] = (datetime.utcnow() - timedelta(days=i+1)).isoformat()
        if sentinel_update:
            app["sentinel_update"] = sentinel_update
        if deadline:
            app["deadline"] = deadline
        applications.append(app)
    
    return applications
