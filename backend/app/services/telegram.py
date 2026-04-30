"""Telegram Bot service"""

import httpx
from typing import Optional, Dict, Any, List

from app.config import settings


class TelegramService:
    """Service for sending Telegram messages"""
    
    def __init__(self):
        self.token = settings.telegram_bot_token
        self.base_url = f"https://api.telegram.org/bot{self.token}"
    
    async def send_message(
        self,
        chat_id: int,
        text: str,
        parse_mode: str = "HTML",
        reply_markup: Optional[Dict] = None,
    ) -> bool:
        """Send a text message"""
        if not self.token:
            print("[Telegram] Bot token not configured")
            return False
        
        payload = {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": parse_mode,
        }
        
        if reply_markup:
            payload["reply_markup"] = reply_markup
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/sendMessage",
                    json=payload,
                    timeout=10.0,
                )
                return response.status_code == 200
        except Exception as e:
            print(f"[Telegram] Send error: {e}")
            return False
    
    async def send_job_card(
        self,
        chat_id: int,
        job_id: str,
        company: str,
        title: str,
        location: str,
        salary_min: Optional[int],
        salary_max: Optional[int],
        match_score: int,
        job_url: str,
    ) -> bool:
        """Send a job card with approve/reject buttons"""
        
        # Format salary
        salary = "Not specified"
        if salary_min and salary_max:
            salary = f"${salary_min:,} - ${salary_max:,}"
        elif salary_min:
            salary = f"${salary_min:,}+"
        
        # Score emoji
        if match_score >= 85:
            score_emoji = "🎯"
        elif match_score >= 70:
            score_emoji = "✅"
        else:
            score_emoji = "📋"
        
        text = f"""{score_emoji} <b>{match_score}% Match</b>

<b>{title}</b>
🏢 {company}
📍 {location}
💰 {salary}

<a href="{job_url}">View Job Post</a>"""
        
        # Inline keyboard with approve/reject buttons
        keyboard = {
            "inline_keyboard": [
                [
                    {"text": "✅ Apply", "callback_data": f"approve_{job_id}"},
                    {"text": "❌ Skip", "callback_data": f"reject_{job_id}"},
                ],
                [
                    {"text": "📋 Details", "callback_data": f"view_{job_id}"},
                ],
            ]
        }
        
        return await self.send_message(chat_id, text, reply_markup=keyboard)
    
    async def answer_callback(self, callback_id: str, text: str = "") -> bool:
        """Answer a callback query"""
        if not self.token:
            return False
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/answerCallbackQuery",
                    json={
                        "callback_query_id": callback_id,
                        "text": text,
                    },
                    timeout=10.0,
                )
                return response.status_code == 200
        except Exception as e:
            print(f"[Telegram] Callback error: {e}")
            return False
    
    async def send_alert(
        self,
        chat_id: int,
        alert_type: str,
        company: str,
        message: str,
        priority: str = "normal",
    ) -> bool:
        """Send a priority alert"""
        emoji_map = {
            "interview": "🎯",
            "offer": "🎉",
            "assessment": "📝",
            "deadline": "⚠️",
            "rejection": "📭",
        }
        
        priority_prefix = "🚨 " if priority == "urgent" else ""
        emoji = emoji_map.get(alert_type, "📬")
        
        text = f"""{priority_prefix}{emoji} <b>{alert_type.upper()}</b>

🏢 {company}

{message}"""
        
        return await self.send_message(chat_id, text)
