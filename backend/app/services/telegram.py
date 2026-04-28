"""
Telegram Bot Service for JobSniper AI
Handles sending job notifications and receiving approval responses
"""
import os
import httpx
from typing import Optional
from app.config import settings


class TelegramBot:
    """Telegram Bot client for sending notifications"""
    
    def __init__(self):
        self.token = settings.TELEGRAM_BOT_TOKEN
        self.base_url = f"https://api.telegram.org/bot{self.token}" if self.token else None
    
    @property
    def is_configured(self) -> bool:
        return self.token is not None and len(self.token) > 0
    
    async def send_message(
        self,
        chat_id: str,
        text: str,
        parse_mode: str = "HTML",
        reply_markup: Optional[dict] = None
    ) -> dict | None:
        """Send a message to a Telegram chat"""
        if not self.is_configured:
            print("[TelegramBot] Not configured, skipping message")
            return None
        
        payload = {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": parse_mode
        }
        
        if reply_markup:
            payload["reply_markup"] = reply_markup
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{self.base_url}/sendMessage",
                    json=payload,
                    timeout=10.0
                )
                return response.json()
            except Exception as e:
                print(f"[TelegramBot] Error sending message: {e}")
                return None
    
    async def send_job_notification(
        self,
        chat_id: str,
        job: dict,
        match_score: int,
        application_id: str
    ) -> dict | None:
        """Send a job opportunity notification with approval buttons"""
        
        salary_text = ""
        if job.get("salary_min") and job.get("salary_max"):
            salary_text = f"\n💰 <b>Salary:</b> ${job['salary_min']:,} - ${job['salary_max']:,}"
        elif job.get("salary_min"):
            salary_text = f"\n💰 <b>Salary:</b> ${job['salary_min']:,}+"
        
        message = f"""
🎯 <b>New Job Match!</b> ({match_score}% match)

<b>{job['title']}</b>
🏢 {job['company']}
📍 {job.get('location', 'Remote')}{salary_text}

{job.get('description', '')[:300]}{'...' if len(job.get('description', '')) > 300 else ''}

<a href="{job['job_url']}">View Full Job Posting</a>
"""
        
        # Inline keyboard for approval
        reply_markup = {
            "inline_keyboard": [
                [
                    {"text": "✅ Apply", "callback_data": f"approve_{application_id}"},
                    {"text": "❌ Skip", "callback_data": f"reject_{application_id}"}
                ],
                [
                    {"text": "⏰ Later", "callback_data": f"later_{application_id}"}
                ]
            ]
        }
        
        return await self.send_message(chat_id, message, reply_markup=reply_markup)
    
    async def send_status_update(
        self,
        chat_id: str,
        company: str,
        status: str,
        details: Optional[str] = None
    ) -> dict | None:
        """Send a status update notification"""
        
        status_emoji = {
            "under_review": "👀",
            "assessment": "📝",
            "interview_scheduled": "📅",
            "interview": "🎤",
            "offer": "🎉",
            "rejected": "😔"
        }
        
        emoji = status_emoji.get(status, "📬")
        status_text = status.replace("_", " ").title()
        
        message = f"""
{emoji} <b>Application Update</b>

🏢 <b>{company}</b>
📊 Status: <b>{status_text}</b>
"""
        
        if details:
            message += f"\n📝 {details}"
        
        return await self.send_message(chat_id, message)
    
    async def send_interview_alert(
        self,
        chat_id: str,
        company: str,
        interview_type: str,
        scheduled_time: Optional[str] = None,
        calendly_link: Optional[str] = None
    ) -> dict | None:
        """Send high-priority interview alert"""
        
        message = f"""
🚨 <b>INTERVIEW ALERT!</b> 🚨

🏢 <b>{company}</b>
📋 Type: {interview_type}
"""
        
        if scheduled_time:
            message += f"\n🗓️ Time: {scheduled_time}"
        
        if calendly_link:
            message += f"\n\n<a href=\"{calendly_link}\">📅 Schedule Now</a>"
        
        return await self.send_message(chat_id, message)
    
    async def send_deadline_reminder(
        self,
        chat_id: str,
        company: str,
        deadline: str,
        task_type: str
    ) -> dict | None:
        """Send deadline reminder"""
        
        message = f"""
⏰ <b>Deadline Reminder!</b>

🏢 <b>{company}</b>
📋 Task: {task_type}
📅 Due: <b>{deadline}</b>

Don't miss this opportunity!
"""
        
        return await self.send_message(chat_id, message)


# Singleton instance
telegram_bot = TelegramBot()
