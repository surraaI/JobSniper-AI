"""
OpenAI Service for JobSniper AI
Handles all LLM interactions for agents
"""
import os
from openai import AsyncOpenAI
from typing import Optional
from app.config import settings


class OpenAIService:
    """OpenAI client for agent LLM calls"""
    
    def __init__(self):
        self.api_key = settings.OPENAI_API_KEY
        self.client = AsyncOpenAI(api_key=self.api_key) if self.api_key else None
        self.model = "gpt-4o"
    
    @property
    def is_configured(self) -> bool:
        return self.api_key is not None and len(self.api_key) > 0
    
    async def chat_completion(
        self,
        messages: list[dict],
        temperature: float = 0.7,
        max_tokens: int = 2000,
        json_mode: bool = False
    ) -> str | None:
        """Get a chat completion from OpenAI"""
        if not self.is_configured:
            print("[OpenAI] Not configured, returning mock response")
            return None
        
        try:
            kwargs = {
                "model": self.model,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens
            }
            
            if json_mode:
                kwargs["response_format"] = {"type": "json_object"}
            
            response = await self.client.chat.completions.create(**kwargs)
            return response.choices[0].message.content
        except Exception as e:
            print(f"[OpenAI] Error: {e}")
            return None
    
    async def analyze_job_match(
        self,
        job: dict,
        profile: dict
    ) -> dict:
        """Analyze how well a job matches a user profile"""
        
        system_prompt = """You are an expert career advisor analyzing job fit.
Analyze the job posting against the candidate's profile and return a JSON object with:
- match_score: integer 0-100
- strengths: list of matching qualifications
- gaps: list of missing qualifications
- recommendation: brief recommendation text
- priority: "high", "medium", or "low"
"""
        
        user_prompt = f"""
JOB POSTING:
Title: {job.get('title')}
Company: {job.get('company')}
Description: {job.get('description', '')}
Requirements: {job.get('requirements', [])}

CANDIDATE PROFILE:
Skills: {profile.get('skills', [])}
Experience: {profile.get('experience_years', 0)} years
Target Roles: {profile.get('preferences', {}).get('target_roles', [])}
"""
        
        response = await self.chat_completion(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            json_mode=True
        )
        
        if response:
            import json
            try:
                return json.loads(response)
            except:
                pass
        
        # Fallback mock response
        return {
            "match_score": 75,
            "strengths": ["Relevant experience", "Strong technical skills"],
            "gaps": ["Missing specific certification"],
            "recommendation": "Good match overall. Consider highlighting transferable skills.",
            "priority": "medium"
        }
    
    async def generate_cover_letter(
        self,
        job: dict,
        profile: dict,
        style: str = "professional"
    ) -> str:
        """Generate a tailored cover letter"""
        
        system_prompt = f"""You are an expert career writer creating compelling cover letters.
Write in a {style} tone. The letter should:
- Be 3-4 paragraphs
- Highlight relevant experience
- Show enthusiasm for the company
- Include a strong call to action
"""
        
        user_prompt = f"""
Write a cover letter for this job:

POSITION: {job.get('title')} at {job.get('company')}
DESCRIPTION: {job.get('description', '')}

CANDIDATE:
Name: {profile.get('full_name', 'Candidate')}
Skills: {profile.get('skills', [])}
Experience: {profile.get('experience_years', 0)} years
"""
        
        response = await self.chat_completion(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        )
        
        if response:
            return response
        
        # Fallback
        return f"""Dear Hiring Manager,

I am excited to apply for the {job.get('title')} position at {job.get('company')}. With {profile.get('experience_years', 'several')} years of experience, I am confident I can make valuable contributions to your team.

My background in {', '.join(profile.get('skills', ['technology'])[:3])} aligns well with your requirements. I am particularly drawn to {job.get('company')}'s mission and would welcome the opportunity to contribute.

I look forward to discussing how my experience can benefit your team.

Best regards,
{profile.get('full_name', 'Candidate')}
"""
    
    async def tailor_resume(
        self,
        job: dict,
        resume_text: str
    ) -> str:
        """Suggest resume improvements for a specific job"""
        
        system_prompt = """You are an expert resume consultant.
Analyze the resume against the job posting and provide specific suggestions to tailor it.
Return bullet points of actionable improvements."""
        
        user_prompt = f"""
JOB POSTING:
{job.get('title')} at {job.get('company')}
{job.get('description', '')}

CURRENT RESUME:
{resume_text[:3000]}
"""
        
        response = await self.chat_completion(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        )
        
        return response or "• Highlight relevant experience\n• Add keywords from job description\n• Quantify achievements"
    
    async def generate_outreach_message(
        self,
        job: dict,
        profile: dict,
        recruiter_name: Optional[str] = None
    ) -> str:
        """Generate a LinkedIn/email outreach message"""
        
        greeting = f"Hi {recruiter_name}," if recruiter_name else "Hi there,"
        
        system_prompt = """You are an expert at writing personalized outreach messages.
Write a brief, friendly message (2-3 sentences) that:
- Shows genuine interest in the role
- Highlights one key qualification
- Invites further conversation
Keep it under 100 words."""
        
        user_prompt = f"""
Write an outreach message for:
Position: {job.get('title')} at {job.get('company')}
Candidate Skills: {', '.join(profile.get('skills', [])[:5])}
Experience: {profile.get('experience_years', 0)} years
"""
        
        response = await self.chat_completion(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=200
        )
        
        if response:
            return f"{greeting}\n\n{response}"
        
        return f"""{greeting}

I noticed your {job.get('title')} opening and wanted to reach out. With {profile.get('experience_years', 'several')} years of experience in {profile.get('skills', ['the field'])[0] if profile.get('skills') else 'the field'}, I'd love to discuss how I could contribute to {job.get('company')}.

Would you be open to a brief chat?

Best,
{profile.get('full_name', 'Candidate')}
"""
    
    async def analyze_email(self, email_content: str) -> dict:
        """Analyze an email for job-related updates"""
        
        system_prompt = """You are an email analyzer for job applications.
Analyze the email and return a JSON object with:
- is_job_related: boolean
- category: "interview_invite", "assessment", "status_update", "rejection", "offer", "other"
- company: extracted company name or null
- action_required: boolean
- deadline: extracted deadline or null
- calendly_link: extracted scheduling link or null
- summary: brief summary of the email
"""
        
        response = await self.chat_completion(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Analyze this email:\n\n{email_content[:2000]}"}
            ],
            json_mode=True
        )
        
        if response:
            import json
            try:
                return json.loads(response)
            except:
                pass
        
        return {
            "is_job_related": False,
            "category": "other",
            "company": None,
            "action_required": False,
            "deadline": None,
            "calendly_link": None,
            "summary": "Could not analyze email"
        }


# Singleton instance
openai_service = OpenAIService()
