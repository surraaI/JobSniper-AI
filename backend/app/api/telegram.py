"""Telegram Bot API endpoints"""

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from typing import Optional
import json

from app.services.telegram import TelegramService
from app.services.supabase import get_client
from app.config import settings

router = APIRouter()
telegram = TelegramService()


class WebhookUpdate(BaseModel):
    update_id: int
    message: Optional[dict] = None
    callback_query: Optional[dict] = None


@router.post("/webhook")
async def telegram_webhook(request: Request):
    """Handle incoming Telegram updates"""
    try:
        data = await request.json()
        
        if "message" in data:
            await handle_message(data["message"])
        elif "callback_query" in data:
            await handle_callback(data["callback_query"])
        
        return {"ok": True}
    except Exception as e:
        print(f"[v0] Telegram webhook error: {e}")
        return {"ok": False, "error": str(e)}


async def handle_message(message: dict):
    """Handle incoming text messages"""
    chat_id = message["chat"]["id"]
    text = message.get("text", "")
    
    if text.startswith("/start"):
        # Extract user_id if passed as parameter
        parts = text.split()
        if len(parts) > 1:
            user_id = parts[1]
            # Link Telegram to user account
            try:
                client = await get_client()
                await client.table("profiles").update({
                    "telegram_chat_id": str(chat_id)
                }).eq("id", user_id).execute()
                
                await telegram.send_message(
                    chat_id,
                    "Successfully connected to JobSniper AI!\n\n"
                    "I'll send you job matches for approval and notify you of interview invites.\n\n"
                    "Commands:\n"
                    "/status - View your application stats\n"
                    "/jobs - See pending job matches\n"
                    "/hunt - Start a new job search"
                )
            except Exception as e:
                await telegram.send_message(chat_id, f"Failed to connect: {str(e)}")
        else:
            await telegram.send_message(
                chat_id,
                "Welcome to JobSniper AI!\n\n"
                "To connect your account, please use the link from your dashboard."
            )
    
    elif text.startswith("/status"):
        await handle_status(chat_id)
    
    elif text.startswith("/jobs"):
        await handle_pending_jobs(chat_id)
    
    elif text.startswith("/hunt"):
        await handle_hunt(chat_id, text)
    
    else:
        await telegram.send_message(
            chat_id,
            "Commands:\n"
            "/status - View your stats\n"
            "/jobs - See pending matches\n"
            "/hunt [query] - Start job search"
        )


async def handle_callback(callback: dict):
    """Handle inline button callbacks"""
    chat_id = callback["message"]["chat"]["id"]
    data = callback.get("data", "")
    callback_id = callback["id"]
    
    # Acknowledge the callback
    await telegram.answer_callback(callback_id)
    
    if data.startswith("approve_"):
        job_id = data.replace("approve_", "")
        await handle_approval(chat_id, job_id, approved=True)
    
    elif data.startswith("reject_"):
        job_id = data.replace("reject_", "")
        await handle_approval(chat_id, job_id, approved=False)
    
    elif data.startswith("view_"):
        job_id = data.replace("view_", "")
        await handle_view_job(chat_id, job_id)


async def handle_status(chat_id: int):
    """Send application statistics"""
    try:
        client = await get_client()
        
        # Find user by telegram_chat_id
        profile = await client.table("profiles").select("id").eq("telegram_chat_id", str(chat_id)).single().execute()
        
        if not profile.data:
            await telegram.send_message(chat_id, "Account not connected. Please link from dashboard.")
            return
        
        user_id = profile.data["id"]
        
        # Get stats
        apps = await client.table("applications").select("status").eq("user_id", user_id).execute()
        
        stats = {"total": 0, "pending": 0, "applied": 0, "interviews": 0, "offers": 0}
        for app in apps.data:
            stats["total"] += 1
            status = app["status"]
            if status == "pending_approval":
                stats["pending"] += 1
            elif status in ["applied", "under_review"]:
                stats["applied"] += 1
            elif status in ["interview", "interview_scheduled", "assessment"]:
                stats["interviews"] += 1
            elif status == "offer":
                stats["offers"] += 1
        
        await telegram.send_message(
            chat_id,
            f"📊 Your JobSniper Stats\n\n"
            f"Total Applications: {stats['total']}\n"
            f"⏳ Pending Approval: {stats['pending']}\n"
            f"📤 Applied: {stats['applied']}\n"
            f"🎯 Interviews: {stats['interviews']}\n"
            f"🎉 Offers: {stats['offers']}"
        )
    except Exception as e:
        await telegram.send_message(chat_id, f"Error: {str(e)}")


async def handle_pending_jobs(chat_id: int):
    """Send pending job matches for approval"""
    try:
        client = await get_client()
        
        profile = await client.table("profiles").select("id").eq("telegram_chat_id", str(chat_id)).single().execute()
        
        if not profile.data:
            await telegram.send_message(chat_id, "Account not connected.")
            return
        
        user_id = profile.data["id"]
        
        # Get pending applications
        apps = await client.table("applications").select("*, jobs(*)").eq("user_id", user_id).eq("status", "pending_approval").order("match_score", desc=True).limit(5).execute()
        
        if not apps.data:
            await telegram.send_message(chat_id, "No pending job matches. Run /hunt to find new opportunities!")
            return
        
        for app in apps.data:
            job = app.get("jobs", {})
            await telegram.send_job_card(
                chat_id,
                job_id=app["job_id"],
                company=job.get("company", "Unknown"),
                title=job.get("title", "Unknown"),
                location=job.get("location", "Remote"),
                salary_min=job.get("salary_min"),
                salary_max=job.get("salary_max"),
                match_score=app.get("match_score", 0),
                job_url=job.get("job_url", ""),
            )
    except Exception as e:
        await telegram.send_message(chat_id, f"Error: {str(e)}")


async def handle_approval(chat_id: int, job_id: str, approved: bool):
    """Handle job approval/rejection"""
    try:
        client = await get_client()
        
        profile = await client.table("profiles").select("id").eq("telegram_chat_id", str(chat_id)).single().execute()
        user_id = profile.data["id"]
        
        new_status = "approved" if approved else "withdrawn"
        
        await client.table("applications").update({
            "status": new_status
        }).eq("user_id", user_id).eq("job_id", job_id).execute()
        
        emoji = "✅" if approved else "❌"
        action = "approved for application" if approved else "skipped"
        await telegram.send_message(chat_id, f"{emoji} Job {action}!")
        
    except Exception as e:
        await telegram.send_message(chat_id, f"Error: {str(e)}")


async def handle_hunt(chat_id: int, text: str):
    """Trigger a new job hunt"""
    try:
        client = await get_client()
        
        profile = await client.table("profiles").select("*").eq("telegram_chat_id", str(chat_id)).single().execute()
        
        if not profile.data:
            await telegram.send_message(chat_id, "Account not connected.")
            return
        
        await telegram.send_message(chat_id, "🔍 Scout agent activated! Searching for jobs...")
        
        # Parse query from command
        parts = text.split(maxsplit=1)
        query = parts[1] if len(parts) > 1 else None
        
        from app.agents.scout import ScoutAgent
        scout = ScoutAgent()
        
        jobs = await scout.hunt(query=query, limit=10)
        
        await telegram.send_message(
            chat_id,
            f"Found {len(jobs)} matching jobs!\n"
            f"Use /jobs to review and approve applications."
        )
        
    except Exception as e:
        await telegram.send_message(chat_id, f"Error: {str(e)}")


async def handle_view_job(chat_id: int, job_id: str):
    """Send detailed job info"""
    try:
        client = await get_client()
        job = await client.table("jobs").select("*").eq("id", job_id).single().execute()
        
        if job.data:
            j = job.data
            await telegram.send_message(
                chat_id,
                f"📋 {j.get('title')}\n"
                f"🏢 {j.get('company')}\n"
                f"📍 {j.get('location', 'Not specified')}\n\n"
                f"{j.get('description', 'No description')[:500]}...\n\n"
                f"🔗 {j.get('job_url')}"
            )
    except Exception as e:
        await telegram.send_message(chat_id, f"Error: {str(e)}")
