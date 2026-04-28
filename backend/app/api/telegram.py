"""
Telegram Bot API endpoints
"""
from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from typing import Optional

router = APIRouter()


class TelegramWebhook(BaseModel):
    update_id: int
    message: Optional[dict] = None
    callback_query: Optional[dict] = None


class ConnectTelegramRequest(BaseModel):
    user_id: str
    telegram_username: str


@router.post("/webhook")
async def telegram_webhook(request: Request):
    """
    Webhook endpoint for Telegram bot updates.
    Handles:
    - /start - Connect account
    - Callback queries - Job approvals/rejections
    """
    body = await request.json()
    
    # Handle callback queries (button presses)
    if "callback_query" in body:
        callback = body["callback_query"]
        data = callback.get("data", "")
        
        if data.startswith("approve_"):
            job_id = data.replace("approve_", "")
            # TODO: Approve job, trigger Ghostwriter
            return {"status": "approved", "job_id": job_id}
        
        elif data.startswith("reject_"):
            job_id = data.replace("reject_", "")
            # TODO: Reject job
            return {"status": "rejected", "job_id": job_id}
        
        elif data.startswith("details_"):
            job_id = data.replace("details_", "")
            # TODO: Send full job details
            return {"status": "details_sent", "job_id": job_id}
    
    # Handle messages
    if "message" in body:
        message = body["message"]
        text = message.get("text", "")
        chat_id = message["chat"]["id"]
        
        if text == "/start":
            # TODO: Send welcome message with connection instructions
            return {
                "status": "welcome_sent",
                "chat_id": chat_id,
                "message": "Welcome to JobSniper AI!"
            }
        
        elif text == "/status":
            # TODO: Send current agent status
            return {"status": "status_sent", "chat_id": chat_id}
        
        elif text == "/jobs":
            # TODO: Send pending jobs for approval
            return {"status": "jobs_sent", "chat_id": chat_id}
    
    return {"status": "ok"}


@router.post("/connect")
async def connect_telegram(request: ConnectTelegramRequest):
    """
    Connect a user's account to their Telegram.
    """
    # TODO: Generate connection code, store in Supabase
    return {
        "success": True,
        "message": "Connection initiated",
        "instructions": f"Send /connect {request.user_id[:8]} to @JobSniperAIBot"
    }


@router.get("/status/{user_id}")
async def get_telegram_status(user_id: str):
    """
    Check if user has connected Telegram.
    """
    # TODO: Check Supabase for telegram_chat_id
    return {
        "success": True,
        "connected": False,
        "message": "Telegram not connected. Connect to receive job notifications."
    }


@router.post("/send-job/{user_id}")
async def send_job_to_telegram(user_id: str, job_id: str):
    """
    Send a job opportunity to user's Telegram for approval.
    """
    # TODO: Fetch job, send to Telegram with inline buttons
    return {
        "success": True,
        "message": "Job sent to Telegram",
        "job_id": job_id
    }
