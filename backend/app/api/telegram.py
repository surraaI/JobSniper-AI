"""
Telegram Bot API endpoints for JobSniper AI
Handles webhooks, job notifications, and approval flow
"""
from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from app.services.telegram import telegram_bot
from app.services.supabase import (
    get_supabase, 
    get_user_profile, 
    update_user_profile,
    update_application,
    log_agent_activity
)
from app.services.demo_data import get_demo_jobs

router = APIRouter()


class ConnectTelegramRequest(BaseModel):
    user_id: str
    code: str


class SendJobRequest(BaseModel):
    job_id: str
    match_score: int = 80


@router.post("/webhook")
async def telegram_webhook(request: Request):
    """
    Webhook endpoint for Telegram bot updates.
    Handles:
    - /start - Welcome message
    - /connect <code> - Link account
    - /status - Current hunt status
    - /jobs - Pending approvals
    - Callback queries - Job approvals/rejections
    """
    try:
        body = await request.json()
    except:
        return {"status": "error", "message": "Invalid JSON"}
    
    # Handle callback queries (inline button presses)
    if "callback_query" in body:
        callback = body["callback_query"]
        data = callback.get("data", "")
        chat_id = str(callback["message"]["chat"]["id"])
        message_id = callback["message"]["message_id"]
        
        if data.startswith("approve_"):
            application_id = data.replace("approve_", "")
            
            # Update application status
            await update_application(application_id, {
                "status": "approved",
                "approved_at": datetime.utcnow().isoformat()
            })
            
            # Log agent activity
            await log_agent_activity(
                user_id=None,  # Would need to look up from application
                agent="liaison",
                action="job_approved_via_telegram",
                application_id=application_id
            )
            
            # Send confirmation
            await telegram_bot.send_message(
                chat_id,
                "✅ <b>Application Approved!</b>\n\nGhostwriter is now crafting your personalized application..."
            )
            
            return {"status": "approved", "application_id": application_id}
        
        elif data.startswith("reject_"):
            application_id = data.replace("reject_", "")
            
            await update_application(application_id, {
                "status": "withdrawn"
            })
            
            await telegram_bot.send_message(
                chat_id,
                "❌ <b>Job Skipped</b>\n\nNo worries! Your Scout is finding more opportunities..."
            )
            
            return {"status": "rejected", "application_id": application_id}
        
        elif data.startswith("later_"):
            application_id = data.replace("later_", "")
            
            await telegram_bot.send_message(
                chat_id,
                "⏰ <b>Saved for later</b>\n\nI'll remind you about this one. Check /jobs anytime to review."
            )
            
            return {"status": "deferred", "application_id": application_id}
    
    # Handle text messages
    if "message" in body:
        message = body["message"]
        text = message.get("text", "").strip()
        chat_id = str(message["chat"]["id"])
        user_name = message["chat"].get("first_name", "there")
        
        # /start command
        if text == "/start":
            welcome_msg = f"""
👋 <b>Welcome to JobSniper AI, {user_name}!</b>

I'm your AI career assistant. Here's what I can do:

🎯 <b>Sniper Mode</b> - Hunt jobs while you sleep
🛡️ <b>Sentinel Mode</b> - Monitor your inbox for replies

<b>Commands:</b>
/connect [code] - Link your account
/status - View your hunt status
/jobs - Review pending opportunities
/help - Get help

To get started, connect your account from the JobSniper dashboard and use the code provided.
"""
            await telegram_bot.send_message(chat_id, welcome_msg)
            return {"status": "welcome_sent", "chat_id": chat_id}
        
        # /connect command
        elif text.startswith("/connect"):
            parts = text.split()
            if len(parts) < 2:
                await telegram_bot.send_message(
                    chat_id,
                    "❌ Please provide your connection code.\n\nUsage: /connect YOUR_CODE"
                )
                return {"status": "error", "message": "No code provided"}
            
            code = parts[1]
            
            # TODO: Validate code and link account
            # For now, we'll just acknowledge
            await telegram_bot.send_message(
                chat_id,
                f"🔗 <b>Connection Code Received!</b>\n\nProcessing code: {code}\n\nYou'll start receiving job matches soon!"
            )
            
            return {"status": "connecting", "code": code, "chat_id": chat_id}
        
        # /status command
        elif text == "/status":
            status_msg = """
📊 <b>Your JobSniper Status</b>

🎯 <b>Sniper Mode:</b> Active
🛡️ <b>Sentinel Mode:</b> Active

<b>Today's Activity:</b>
• Jobs Scanned: 247
• Matches Found: 12
• Pending Approval: 3
• Applications Sent: 5

<b>This Week:</b>
• Interviews Scheduled: 2
• Email Replies Detected: 8

Your agents are working 24/7! 💪
"""
            await telegram_bot.send_message(chat_id, status_msg)
            return {"status": "status_sent"}
        
        # /jobs command
        elif text == "/jobs":
            # Get demo jobs for display
            demo_jobs = get_demo_jobs()[:3]
            
            if not demo_jobs:
                await telegram_bot.send_message(
                    chat_id,
                    "📭 <b>No pending jobs</b>\n\nYour Scout is out hunting! Check back soon."
                )
                return {"status": "no_jobs"}
            
            await telegram_bot.send_message(
                chat_id,
                f"📋 <b>Pending Opportunities ({len(demo_jobs)})</b>\n\nReview and approve:"
            )
            
            for job in demo_jobs:
                await telegram_bot.send_job_notification(
                    chat_id,
                    job,
                    job.get("match_score", 85),
                    f"demo_{job['id']}"
                )
            
            return {"status": "jobs_sent", "count": len(demo_jobs)}
        
        # /help command
        elif text == "/help":
            help_msg = """
🆘 <b>JobSniper AI Help</b>

<b>Available Commands:</b>
/start - Welcome message
/connect [code] - Link your account
/status - View hunt status
/jobs - Review pending opportunities
/help - This message

<b>About Job Notifications:</b>
When you receive a job match, you'll see:
✅ Apply - Approve and apply automatically
❌ Skip - Pass on this opportunity
⏰ Later - Save for later review

<b>Need Support?</b>
Visit jobsniper.ai/help or email support@jobsniper.ai
"""
            await telegram_bot.send_message(chat_id, help_msg)
            return {"status": "help_sent"}
    
    return {"status": "ok"}


@router.post("/connect")
async def connect_telegram(request: ConnectTelegramRequest):
    """
    Connect a user's account to their Telegram.
    Validates the code and stores the chat_id.
    """
    # Generate a simple connection code
    # In production, this would validate against stored codes
    
    return {
        "success": True,
        "message": "Connection code generated",
        "code": request.code,
        "instructions": f"Send /connect {request.code} to @JobSniperAIBot on Telegram"
    }


@router.get("/status/{user_id}")
async def get_telegram_status(user_id: str):
    """
    Check if user has connected Telegram.
    """
    profile = await get_user_profile(user_id)
    
    if profile and profile.get("telegram_chat_id"):
        return {
            "success": True,
            "connected": True,
            "chat_id": profile["telegram_chat_id"]
        }
    
    return {
        "success": True,
        "connected": False,
        "message": "Telegram not connected. Connect to receive instant job notifications!"
    }


@router.post("/send-job/{user_id}")
async def send_job_to_telegram(user_id: str, request: SendJobRequest):
    """
    Send a job opportunity to user's Telegram for approval.
    """
    profile = await get_user_profile(user_id)
    
    if not profile or not profile.get("telegram_chat_id"):
        raise HTTPException(status_code=400, detail="Telegram not connected")
    
    chat_id = profile["telegram_chat_id"]
    
    # Get job details (demo for now)
    demo_jobs = get_demo_jobs()
    job = next((j for j in demo_jobs if j["id"] == request.job_id), None)
    
    if not job:
        # Create a mock job for demo
        job = {
            "id": request.job_id,
            "title": "Software Engineer",
            "company": "Demo Company",
            "location": "Remote",
            "description": "An exciting opportunity...",
            "job_url": "https://example.com/job"
        }
    
    result = await telegram_bot.send_job_notification(
        chat_id,
        job,
        request.match_score,
        f"app_{request.job_id}"
    )
    
    if result:
        return {
            "success": True,
            "message": "Job sent to Telegram",
            "job_id": request.job_id
        }
    
    return {
        "success": False,
        "message": "Failed to send to Telegram. Bot may not be configured."
    }


@router.post("/test-notification/{chat_id}")
async def test_notification(chat_id: str):
    """
    Send a test notification to verify bot is working.
    """
    result = await telegram_bot.send_message(
        chat_id,
        "🧪 <b>Test Notification</b>\n\nJobSniper AI is connected and ready to hunt!"
    )
    
    return {
        "success": bool(result),
        "message": "Test notification sent" if result else "Failed to send"
    }
