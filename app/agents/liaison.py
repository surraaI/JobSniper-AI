"""
Liaison Agent - Application Submission
Handles the actual submission of applications to job boards.
"""
from typing import Optional
from datetime import datetime

from app.config import get_settings


class LiaisonAgent:
    """
    The Liaison Agent handles the submission of approved applications.
    
    Responsibilities:
    - Submit applications via job board APIs
    - Send outreach messages to recruiters
    - Track submission status
    - Handle follow-ups
    """
    
    def __init__(self):
        self.settings = get_settings()
    
    async def submit_application(
        self,
        job: dict,
        user_profile: dict,
        cover_letter: str,
        resume_highlights: list[str]
    ) -> dict:
        """
        Submit an application for a job.
        
        Returns submission result with status and any error messages.
        """
        source = job.get("source", "unknown")
        
        # Route to appropriate submission handler
        handlers = {
            "adzuna": self._submit_via_redirect,
            "theirstack": self._submit_via_redirect,
            "linkedin": self._submit_linkedin,
            "upwork": self._submit_upwork,
        }
        
        handler = handlers.get(source, self._submit_via_redirect)
        
        try:
            result = await handler(job, user_profile, cover_letter)
            return {
                "success": True,
                "job_id": job.get("id"),
                "submitted_at": datetime.utcnow().isoformat(),
                "method": result.get("method", "redirect"),
                "message": result.get("message", "Application submitted successfully")
            }
        except Exception as e:
            return {
                "success": False,
                "job_id": job.get("id"),
                "error": str(e),
                "message": "Failed to submit application"
            }
    
    async def _submit_via_redirect(
        self,
        job: dict,
        user_profile: dict,
        cover_letter: str
    ) -> dict:
        """
        For jobs that require applying via external site.
        Returns the URL for manual application.
        """
        # In a real implementation, this could:
        # 1. Open the application URL
        # 2. Auto-fill form fields using browser automation
        # 3. Upload resume and cover letter
        
        return {
            "method": "redirect",
            "url": job.get("url"),
            "message": f"Application materials prepared. Apply at: {job.get('url')}"
        }
    
    async def _submit_linkedin(
        self,
        job: dict,
        user_profile: dict,
        cover_letter: str
    ) -> dict:
        """
        Submit application via LinkedIn.
        Note: Would require LinkedIn API access in production.
        """
        # LinkedIn Easy Apply would be handled here
        return {
            "method": "linkedin",
            "message": "LinkedIn Easy Apply prepared"
        }
    
    async def _submit_upwork(
        self,
        job: dict,
        user_profile: dict,
        cover_letter: str
    ) -> dict:
        """
        Submit proposal on Upwork.
        Note: Would require Upwork API access in production.
        """
        return {
            "method": "upwork",
            "message": "Upwork proposal prepared"
        }
    
    async def send_follow_up(
        self,
        job: dict,
        user_profile: dict,
        days_since_application: int
    ) -> dict:
        """
        Send a follow-up message for an application.
        """
        if days_since_application < 7:
            return {
                "success": False,
                "message": "Too early for follow-up. Wait at least 7 days."
            }
        
        # Generate follow-up message
        follow_up = f"""Hi,

I wanted to follow up on my application for the {job.get('position')} role at {job.get('company')} submitted {days_since_application} days ago.

I remain very interested in this opportunity and would welcome the chance to discuss how my background aligns with your needs.

Best regards,
{user_profile.get('full_name', 'Candidate')}"""
        
        return {
            "success": True,
            "message": follow_up,
            "action": "follow_up_prepared"
        }
    
    async def track_application(self, job_id: str, user_id: str) -> dict:
        """
        Get the current status of an application.
        """
        # TODO: Fetch from Supabase
        return {
            "job_id": job_id,
            "user_id": user_id,
            "status": "applied",
            "applied_at": datetime.utcnow().isoformat(),
            "last_activity": datetime.utcnow().isoformat()
        }
