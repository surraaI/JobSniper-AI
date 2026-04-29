"""
Sentinel Agent - Email Monitoring
Monitors inbox for recruiter responses, interview invites, and status updates.
"""
from typing import Optional
from datetime import datetime
import re
from openai import AsyncOpenAI

from app.config import get_settings


class SentinelAgent:
    """
    The Sentinel Agent monitors the user's email inbox for job-related
    communications and extracts actionable information.
    
    Detects:
    - Interview invitations
    - Calendly/scheduling links
    - Technical assessment requests
    - Rejection emails
    - Offer letters
    - Recruiter follow-ups
    """
    
    def __init__(self):
        self.settings = get_settings()
        self.client = AsyncOpenAI(api_key=self.settings.openai_api_key) if self.settings.openai_api_key else None
    
    # Email patterns for quick detection
    CALENDLY_PATTERN = re.compile(r'calendly\.com/[\w\-/]+')
    INTERVIEW_KEYWORDS = [
        'interview', 'schedule', 'availability', 'meet', 'call',
        'zoom', 'teams', 'google meet', 'phone screen'
    ]
    ASSESSMENT_KEYWORDS = [
        'assessment', 'coding challenge', 'take-home', 'technical test',
        'hackerrank', 'codility', 'leetcode', 'codesignal'
    ]
    REJECTION_KEYWORDS = [
        'unfortunately', 'not moving forward', 'other candidates',
        'not a fit', 'position has been filled', 'decided not to proceed'
    ]
    OFFER_KEYWORDS = [
        'offer letter', 'compensation package', 'start date',
        'pleased to offer', 'excited to extend'
    ]
    
    async def analyze_email(self, email: dict) -> dict:
        """
        Analyze an email to detect job-related content and extract actions.
        
        Args:
            email: Dict with keys: subject, from, body, date
        
        Returns:
            Analysis result with type, priority, actions, and extracted data
        """
        subject = email.get("subject", "").lower()
        body = email.get("body", "").lower()
        sender = email.get("from", "")
        full_text = f"{subject} {body}"
        
        # Quick pattern matching first
        result = self._quick_analyze(email, full_text)
        
        # If high priority or ambiguous, use GPT for deeper analysis
        if result["priority"] == "high" or result["type"] == "unknown":
            if self.client:
                try:
                    gpt_result = await self._gpt_analyze(email)
                    result.update(gpt_result)
                except Exception as e:
                    print(f"GPT email analysis failed: {e}")
        
        return result
    
    def _quick_analyze(self, email: dict, full_text: str) -> dict:
        """
        Quick pattern-based email analysis.
        """
        result = {
            "type": "unknown",
            "priority": "low",
            "actions": [],
            "extracted_data": {}
        }
        
        # Check for Calendly links
        calendly_match = self.CALENDLY_PATTERN.search(full_text)
        if calendly_match:
            result["type"] = "interview_invite"
            result["priority"] = "high"
            result["actions"].append("schedule_interview")
            result["extracted_data"]["calendly_link"] = calendly_match.group()
        
        # Check for interview keywords
        if any(kw in full_text for kw in self.INTERVIEW_KEYWORDS):
            result["type"] = "interview_invite"
            result["priority"] = "high"
            if "schedule_interview" not in result["actions"]:
                result["actions"].append("respond_to_scheduling")
        
        # Check for assessment keywords
        if any(kw in full_text for kw in self.ASSESSMENT_KEYWORDS):
            result["type"] = "assessment"
            result["priority"] = "high"
            result["actions"].append("complete_assessment")
            
            # Try to extract deadline
            deadline_match = re.search(
                r'(?:due|deadline|by|before|complete by)[:\s]+([A-Za-z]+\s+\d+|\d+/\d+/\d+|\d+\s+days?)',
                full_text,
                re.IGNORECASE
            )
            if deadline_match:
                result["extracted_data"]["deadline"] = deadline_match.group(1)
        
        # Check for rejection
        if any(kw in full_text for kw in self.REJECTION_KEYWORDS):
            result["type"] = "rejection"
            result["priority"] = "medium"
            result["actions"].append("update_status")
        
        # Check for offer
        if any(kw in full_text for kw in self.OFFER_KEYWORDS):
            result["type"] = "offer"
            result["priority"] = "high"
            result["actions"].append("review_offer")
        
        return result
    
    async def _gpt_analyze(self, email: dict) -> dict:
        """
        Use GPT-4o for deeper email analysis.
        """
        system_prompt = """You are an AI assistant that analyzes job-related emails.
Classify the email and extract key information.

Return JSON with:
{
    "type": "interview_invite" | "assessment" | "rejection" | "offer" | "follow_up" | "status_update" | "other",
    "company": "company name if found",
    "position": "position title if found",
    "summary": "brief summary of what action is needed",
    "deadline": "any deadline mentioned",
    "links": ["any relevant links found"]
}"""

        user_prompt = f"""
Subject: {email.get('subject', '')}
From: {email.get('from', '')}
Body: {email.get('body', '')[:2000]}

Analyze this job-related email."""

        response = await self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.2
        )
        
        import json
        data = json.loads(response.choices[0].message.content)
        
        return {
            "company": data.get("company"),
            "position": data.get("position"),
            "summary": data.get("summary"),
            "extracted_data": {
                "deadline": data.get("deadline"),
                "links": data.get("links", [])
            }
        }
    
    async def generate_alert(self, analysis: dict, email: dict) -> dict:
        """
        Generate a Telegram/WhatsApp alert message based on email analysis.
        """
        priority_emoji = {
            "high": "🔴",
            "medium": "🟡",
            "low": "🟢"
        }
        
        type_headers = {
            "interview_invite": "📅 Interview Invite!",
            "assessment": "📝 Technical Assessment",
            "rejection": "❌ Application Update",
            "offer": "🎉 Offer Received!",
            "follow_up": "📬 Recruiter Follow-up",
            "status_update": "📊 Status Update"
        }
        
        emoji = priority_emoji.get(analysis.get("priority", "low"), "🟢")
        header = type_headers.get(analysis.get("type", "other"), "📧 New Email")
        
        message = f"{emoji} {header}\n\n"
        
        if analysis.get("company"):
            message += f"🏢 {analysis['company']}\n"
        if analysis.get("position"):
            message += f"💼 {analysis['position']}\n"
        
        message += f"\n📧 Subject: {email.get('subject', 'No subject')}\n"
        
        if analysis.get("summary"):
            message += f"\n💡 {analysis['summary']}\n"
        
        if analysis.get("extracted_data", {}).get("deadline"):
            message += f"\n⏰ Deadline: {analysis['extracted_data']['deadline']}\n"
        
        if analysis.get("extracted_data", {}).get("calendly_link"):
            message += f"\n🔗 Schedule: {analysis['extracted_data']['calendly_link']}\n"
        
        # Add action buttons info
        if analysis.get("actions"):
            message += f"\n📌 Actions needed: {', '.join(analysis['actions'])}"
        
        return {
            "message": message,
            "priority": analysis.get("priority", "low"),
            "type": analysis.get("type", "other")
        }
    
    async def batch_process_emails(self, emails: list[dict]) -> list[dict]:
        """
        Process multiple emails and return prioritized results.
        """
        results = []
        for email in emails:
            analysis = await self.analyze_email(email)
            if analysis["type"] != "unknown":
                results.append({
                    "email": email,
                    "analysis": analysis
                })
        
        # Sort by priority (high first)
        priority_order = {"high": 0, "medium": 1, "low": 2}
        results.sort(key=lambda x: priority_order.get(x["analysis"]["priority"], 3))
        
        return results
