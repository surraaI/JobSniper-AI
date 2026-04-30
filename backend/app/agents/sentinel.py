"""
Sentinel Agent - Inbox Guardian
Monitors email for interview invites, status updates, and recruiter responses.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
import re

from app.services.openai import get_completion
from app.services.supabase import get_client
from app.config import settings


class SentinelAgent:
    """The Sentinel - guards your inbox and never misses an opportunity."""
    
    # Patterns for detecting important emails
    INTERVIEW_PATTERNS = [
        r"interview",
        r"calendly",
        r"schedule.*call",
        r"meet.*team",
        r"technical.*screen",
        r"phone.*screen",
        r"video.*call",
        r"zoom.*meeting",
    ]
    
    ASSESSMENT_PATTERNS = [
        r"assessment",
        r"coding.*challenge",
        r"take.*home",
        r"technical.*test",
        r"hackerrank",
        r"codility",
        r"leetcode",
    ]
    
    OFFER_PATTERNS = [
        r"offer",
        r"congratulations",
        r"pleased.*to.*extend",
        r"welcome.*to.*the.*team",
    ]
    
    REJECTION_PATTERNS = [
        r"unfortunately",
        r"not.*moving.*forward",
        r"other.*candidates",
        r"position.*filled",
        r"not.*selected",
    ]
    
    async def monitor(self, user_id: str) -> Dict[str, Any]:
        """
        Monitor for updates and return any findings.
        In production, this would connect to Gmail API.
        For demo, returns simulated updates.
        """
        if settings.demo_mode:
            return self._demo_updates()
        
        # In production, implement Gmail API integration here
        # For now, return empty updates
        return {
            "checked_at": datetime.utcnow().isoformat(),
            "updates": [],
            "alerts": [],
        }
    
    async def analyze_email(self, email_content: str) -> Dict[str, Any]:
        """
        Analyze an email to determine its type and extract key info.
        """
        content_lower = email_content.lower()
        
        # Check patterns
        email_type = "general"
        priority = "normal"
        deadline = None
        action_required = False
        
        # Interview detection
        for pattern in self.INTERVIEW_PATTERNS:
            if re.search(pattern, content_lower):
                email_type = "interview_invite"
                priority = "high"
                action_required = True
                break
        
        # Assessment detection
        if email_type == "general":
            for pattern in self.ASSESSMENT_PATTERNS:
                if re.search(pattern, content_lower):
                    email_type = "assessment"
                    priority = "high"
                    action_required = True
                    deadline = self._extract_deadline(email_content)
                    break
        
        # Offer detection
        if email_type == "general":
            for pattern in self.OFFER_PATTERNS:
                if re.search(pattern, content_lower):
                    email_type = "offer"
                    priority = "urgent"
                    action_required = True
                    break
        
        # Rejection detection
        if email_type == "general":
            for pattern in self.REJECTION_PATTERNS:
                if re.search(pattern, content_lower):
                    email_type = "rejection"
                    priority = "low"
                    break
        
        # Extract additional info using AI if available
        summary = None
        if settings.openai_api_key and not settings.demo_mode:
            try:
                summary = await self._summarize_email(email_content, email_type)
            except:
                pass
        
        return {
            "type": email_type,
            "priority": priority,
            "action_required": action_required,
            "deadline": deadline,
            "summary": summary,
        }
    
    def _extract_deadline(self, content: str) -> Optional[str]:
        """Extract deadline from email content"""
        # Simple date patterns
        date_patterns = [
            r"by\s+(\w+\s+\d{1,2})",
            r"before\s+(\w+\s+\d{1,2})",
            r"deadline[:\s]+(\w+\s+\d{1,2})",
            r"due[:\s]+(\w+\s+\d{1,2})",
        ]
        
        for pattern in date_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                return match.group(1)
        
        return None
    
    async def _summarize_email(self, content: str, email_type: str) -> str:
        """Use AI to summarize the email"""
        prompt = f"""Summarize this {email_type} email in 1-2 sentences. Extract the key action item if any.

EMAIL:
{content[:1000]}

Be concise and focus on what the recipient needs to do."""
        
        return await get_completion(prompt, max_tokens=100)
    
    async def update_application_status(
        self,
        user_id: str,
        company: str,
        new_status: str,
        update_text: str,
        deadline: Optional[str] = None,
    ) -> bool:
        """Update application status based on email detection"""
        try:
            client = await get_client()
            
            # Find matching application by company
            apps = await client.table("applications").select("*, jobs(company)").eq("user_id", user_id).execute()
            
            for app in apps.data:
                if app.get("jobs", {}).get("company", "").lower() == company.lower():
                    update_data = {
                        "status": new_status,
                        "sentinel_update": update_text,
                    }
                    if deadline:
                        update_data["deadline"] = deadline
                    
                    await client.table("applications").update(update_data).eq("id", app["id"]).execute()
                    
                    # Log the update
                    await client.table("agent_logs").insert({
                        "user_id": user_id,
                        "agent": "sentinel",
                        "action": "status_update",
                        "application_id": app["id"],
                        "output_data": {"new_status": new_status, "update": update_text},
                    }).execute()
                    
                    return True
            
            return False
        except Exception as e:
            print(f"[Sentinel] Update error: {e}")
            return False
    
    def _demo_updates(self) -> Dict[str, Any]:
        """Return simulated updates for demo mode"""
        return {
            "checked_at": datetime.utcnow().isoformat(),
            "updates": [
                {
                    "company": "Stripe",
                    "type": "interview_invite",
                    "summary": "Technical interview scheduled for next Tuesday",
                    "priority": "high",
                },
                {
                    "company": "Vercel",
                    "type": "status_update",
                    "summary": "Application moved to next round",
                    "priority": "normal",
                },
            ],
            "alerts": [
                {
                    "message": "Bending Spoons assessment due in 2 days",
                    "priority": "high",
                    "deadline": "2026-05-01",
                }
            ],
        }
