"""
Ghostwriter Agent - Application Materials Generator
Creates tailored resumes and cover letters for each job.
"""
from typing import Optional
from openai import AsyncOpenAI

from app.config import get_settings


class GhostwriterAgent:
    """
    The Ghostwriter Agent crafts personalized application materials
    tailored to each specific job posting.
    
    Generates:
    - Tailored resume highlights
    - Custom cover letters
    - LinkedIn connection messages
    - Recruiter outreach messages
    """
    
    def __init__(self):
        self.settings = get_settings()
        self.client = AsyncOpenAI(api_key=self.settings.openai_api_key) if self.settings.openai_api_key else None
    
    async def generate_cover_letter(
        self,
        job: dict,
        user_profile: dict
    ) -> str:
        """
        Generate a tailored cover letter for a specific job.
        """
        if not self.client:
            return self._template_cover_letter(job, user_profile)
        
        try:
            return await self._gpt_cover_letter(job, user_profile)
        except Exception as e:
            print(f"GPT cover letter failed: {e}")
            return self._template_cover_letter(job, user_profile)
    
    async def _gpt_cover_letter(self, job: dict, user_profile: dict) -> str:
        """
        Use GPT-4o to generate a personalized cover letter.
        """
        system_prompt = """You are an expert career coach and writer. Generate a compelling, 
personalized cover letter that:
1. Opens with a strong hook mentioning the specific company
2. Highlights 2-3 relevant experiences that match the job requirements
3. Shows enthusiasm and cultural fit
4. Closes with a clear call to action

Keep it concise (250-350 words). Be authentic, not generic.
Do NOT use phrases like "I am writing to apply" or "I believe I am a perfect fit"."""

        user_prompt = f"""
Job Details:
- Company: {job.get('company')}
- Position: {job.get('position')}
- Description: {job.get('description', '')[:1500]}

Candidate Profile:
- Name: {user_profile.get('full_name', 'Candidate')}
- Skills: {', '.join(user_profile.get('skills', []))}
- Experience: {user_profile.get('experience_years', 'several')} years
- Resume Summary: {user_profile.get('resume_text', '')[:1000]}

Generate a cover letter that authentically represents this candidate for this specific role."""

        response = await self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7
        )
        
        return response.choices[0].message.content
    
    def _template_cover_letter(self, job: dict, user_profile: dict) -> str:
        """
        Fallback: Template-based cover letter.
        """
        name = user_profile.get("full_name", "Candidate")
        company = job.get("company", "your company")
        position = job.get("position", "this position")
        skills = user_profile.get("skills", [])[:3]
        
        return f"""Dear Hiring Manager,

I am excited to apply for the {position} role at {company}. With my background in {', '.join(skills)}, I am confident I can make a meaningful contribution to your team.

Throughout my career, I have developed strong expertise that aligns well with this opportunity. I am particularly drawn to {company}'s mission and would welcome the chance to bring my skills to your organization.

I would love to discuss how my experience can benefit your team. Thank you for considering my application.

Best regards,
{name}"""
    
    async def generate_resume_highlights(
        self,
        job: dict,
        user_profile: dict
    ) -> list[str]:
        """
        Generate tailored resume bullet points for a specific job.
        """
        if not self.client:
            return user_profile.get("skills", [])[:5]
        
        try:
            system_prompt = """You are a resume optimization expert. Generate 5 powerful, 
quantified resume bullet points that would be most relevant for this job.
Use the STAR method (Situation, Task, Action, Result) where possible.
Each bullet should start with a strong action verb.
Return as a JSON array of strings."""

            user_prompt = f"""
Job: {job.get('position')} at {job.get('company')}
Requirements: {job.get('description', '')[:1000]}

Candidate Skills: {', '.join(user_profile.get('skills', []))}
Experience: {user_profile.get('experience_years')} years

Generate 5 tailored resume bullet points."""

            response = await self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.5
            )
            
            import json
            data = json.loads(response.choices[0].message.content)
            return data.get("bullets", data.get("highlights", []))
        
        except Exception as e:
            print(f"GPT resume highlights failed: {e}")
            return user_profile.get("skills", [])[:5]
    
    async def generate_outreach_message(
        self,
        job: dict,
        user_profile: dict,
        message_type: str = "linkedin"  # "linkedin", "email", "recruiter"
    ) -> str:
        """
        Generate a personalized outreach message.
        """
        if not self.client:
            return self._template_outreach(job, user_profile, message_type)
        
        try:
            templates = {
                "linkedin": "a LinkedIn connection request message (max 200 characters)",
                "email": "a brief email to the hiring manager (150 words max)",
                "recruiter": "a message to a recruiter about this opportunity (100 words max)"
            }
            
            system_prompt = f"""Generate {templates.get(message_type, templates['linkedin'])}.
Be personable, specific to the company, and include a soft ask. No generic phrases."""

            user_prompt = f"""
Company: {job.get('company')}
Role: {job.get('position')}
Candidate: {user_profile.get('full_name')} - {user_profile.get('experience_years')} years experience in {', '.join(user_profile.get('skills', [])[:3])}"""

            response = await self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7
            )
            
            return response.choices[0].message.content
        
        except Exception as e:
            print(f"GPT outreach failed: {e}")
            return self._template_outreach(job, user_profile, message_type)
    
    def _template_outreach(self, job: dict, user_profile: dict, message_type: str) -> str:
        """Fallback template messages."""
        name = user_profile.get("full_name", "").split()[0] if user_profile.get("full_name") else "there"
        company = job.get("company", "your company")
        position = job.get("position", "the open role")
        
        if message_type == "linkedin":
            return f"Hi! I'm interested in the {position} role at {company}. Would love to connect!"
        else:
            return f"Hi, I'm reaching out about the {position} opportunity at {company}. I'd love to learn more about the role."
