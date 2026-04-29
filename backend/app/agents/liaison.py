"""
Liaison Agent - Outreach Specialist
Drafts personalized messages for recruiters and hiring managers.
"""

from typing import Dict, Any

from app.services.openai import get_completion
from app.config import settings


class LiaisonAgent:
    """The Liaison - connects you with the right people."""
    
    async def draft_outreach(
        self,
        profile: Dict[str, Any],
        job: Dict[str, Any],
        platform: str = "linkedin",
    ) -> str:
        """
        Draft a personalized outreach message for LinkedIn or email.
        """
        if settings.demo_mode or not settings.openai_api_key:
            return self._demo_outreach(profile, job, platform)
        
        try:
            prompt = self._build_outreach_prompt(profile, job, platform)
            return await get_completion(prompt, max_tokens=400)
        except Exception as e:
            print(f"[Liaison] Outreach error: {e}")
            return self._demo_outreach(profile, job, platform)
    
    def _build_outreach_prompt(
        self,
        profile: Dict,
        job: Dict,
        platform: str,
    ) -> str:
        """Build prompt for outreach message"""
        char_limit = 300 if platform == "linkedin" else 500
        
        return f"""Write a personalized {platform} message to a recruiter about this job.

CANDIDATE:
- Name: {profile.get('full_name', 'Candidate')}
- Skills: {', '.join(profile.get('skills', [])[:5])}
- Experience: {profile.get('experience_years', 'Several')} years

JOB:
- Title: {job.get('title')}
- Company: {job.get('company')}

Write a {'brief ' if platform == 'linkedin' else ''}professional message that:
1. Opens with a personalized hook (not "I hope this finds you well")
2. Shows genuine interest in the company
3. Highlights 1-2 relevant qualifications
4. Has a soft call to action
5. Is under {char_limit} characters

Tone: Confident, conversational, not desperate. No clichés."""
    
    def _demo_outreach(
        self,
        profile: Dict,
        job: Dict,
        platform: str,
    ) -> str:
        """Generate demo outreach message"""
        name = profile.get("full_name", "").split()[0] if profile.get("full_name") else ""
        company = job.get("company", "your company")
        title = job.get("title", "the role")
        skill = profile.get("skills", ["technology"])[0] if profile.get("skills") else "technology"
        
        if platform == "linkedin":
            return f"""Hi! I noticed {company} is looking for a {title} and I'm genuinely excited about what you're building.

With my background in {skill}, I've tackled similar challenges and would love to bring that experience to your team.

Would you be open to a quick chat about the role?"""
        else:
            return f"""Subject: Excited about the {title} opportunity at {company}

Hi,

I came across the {title} position at {company} and wanted to reach out directly. Your team's work in this space really resonates with me.

With {profile.get('experience_years', 'several')} years of experience in {skill}, I've delivered results that I believe align well with what you're looking for.

I'd love the chance to discuss how I can contribute to {company}'s goals. Would you have 15 minutes for a quick call this week?

Best,
{name}"""
    
    async def draft_followup(
        self,
        profile: Dict[str, Any],
        job: Dict[str, Any],
        context: str = "no_response",
    ) -> str:
        """
        Draft a follow-up message based on context.
        context: 'no_response', 'after_interview', 'thank_you'
        """
        if settings.demo_mode or not settings.openai_api_key:
            return self._demo_followup(profile, job, context)
        
        prompts = {
            "no_response": "a polite follow-up after not hearing back for a week",
            "after_interview": "a thoughtful follow-up after an interview",
            "thank_you": "a thank-you note after an interview",
        }
        
        try:
            prompt = f"""Write {prompts.get(context, prompts['no_response'])} for this job application.

CANDIDATE: {profile.get('full_name', 'Candidate')}
JOB: {job.get('title')} at {job.get('company')}

Keep it brief (under 150 words), professional, and memorable.
No clichés. Sound human, not robotic."""
            
            return await get_completion(prompt, max_tokens=300)
        except Exception as e:
            return self._demo_followup(profile, job, context)
    
    def _demo_followup(self, profile: Dict, job: Dict, context: str) -> str:
        """Generate demo follow-up"""
        company = job.get("company", "your team")
        title = job.get("title", "the role")
        
        if context == "thank_you":
            return f"""Thank you for taking the time to speak with me about the {title} position. I enjoyed learning more about {company}'s vision and the team's approach.

Our conversation reinforced my excitement about this opportunity. I'm confident my experience would enable me to contribute meaningfully from day one.

Looking forward to the next steps!"""
        else:
            return f"""Hi! I wanted to follow up on my application for the {title} role at {company}.

I remain very interested in this opportunity and would welcome the chance to discuss how my background aligns with your needs.

Please let me know if there's any additional information I can provide."""
