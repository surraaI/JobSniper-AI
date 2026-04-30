"""
Ghostwriter Agent - Application Crafter
Generates tailored resumes and cover letters using GPT-4o.
"""

from typing import Dict, Any

from app.services.openai import get_completion
from app.config import settings


class GhostwriterAgent:
    """The Ghostwriter - crafts compelling application materials."""
    
    async def craft_application(
        self,
        profile: Dict[str, Any],
        job: Dict[str, Any],
    ) -> Dict[str, str]:
        """
        Generate tailored cover letter and resume highlights.
        """
        cover_letter = await self.write_cover_letter(profile, job)
        tailored_resume = await self.tailor_resume(profile, job)
        
        return {
            "cover_letter": cover_letter,
            "tailored_resume": tailored_resume,
        }
    
    async def write_cover_letter(
        self,
        profile: Dict[str, Any],
        job: Dict[str, Any],
    ) -> str:
        """Generate a tailored cover letter"""
        if settings.demo_mode or not settings.openai_api_key:
            return self._demo_cover_letter(profile, job)
        
        try:
            prompt = f"""Write a compelling cover letter for this job application.

CANDIDATE:
- Name: {profile.get('full_name', 'Candidate')}
- Skills: {', '.join(profile.get('skills', []))}
- Experience: {profile.get('experience_years', 'Several')} years
- Background: {profile.get('resume_text', '')[:1000]}

JOB:
- Title: {job.get('title')}
- Company: {job.get('company')}
- Description: {job.get('description', '')[:1500]}

Write a professional, engaging cover letter that:
1. Opens with a strong hook
2. Highlights relevant experience
3. Shows enthusiasm for the company
4. Ends with a clear call to action
5. Is 250-350 words

Use a confident but not arrogant tone. Be specific about skills that match."""
            
            return await get_completion(prompt, max_tokens=800)
        except Exception as e:
            print(f"[Ghostwriter] Cover letter error: {e}")
            return self._demo_cover_letter(profile, job)
    
    async def tailor_resume(
        self,
        profile: Dict[str, Any],
        job: Dict[str, Any],
    ) -> str:
        """Generate tailored resume highlights/summary"""
        if settings.demo_mode or not settings.openai_api_key:
            return self._demo_resume_summary(profile, job)
        
        try:
            prompt = f"""Create a tailored professional summary and key achievements for this job.

CANDIDATE RESUME:
{profile.get('resume_text', 'Experienced professional')}

TARGET JOB:
- Title: {job.get('title')}
- Company: {job.get('company')}
- Requirements: {job.get('description', '')[:1000]}

Create:
1. A compelling 3-4 sentence professional summary tailored to this role
2. 4-5 key achievements that align with the job requirements
3. Suggested skills to emphasize

Format as plain text, ready to insert into a resume."""
            
            return await get_completion(prompt, max_tokens=600)
        except Exception as e:
            print(f"[Ghostwriter] Resume error: {e}")
            return self._demo_resume_summary(profile, job)
    
    def _demo_cover_letter(self, profile: Dict, job: Dict) -> str:
        """Generate a demo cover letter"""
        name = profile.get("full_name", "Applicant")
        company = job.get("company", "your company")
        title = job.get("title", "this position")
        skills = profile.get("skills", ["problem-solving", "collaboration"])[:3]
        
        return f"""Dear Hiring Manager,

I am excited to apply for the {title} position at {company}. With my background in {', '.join(skills)}, I am confident I can make a meaningful contribution to your team.

Throughout my career, I have consistently delivered results by combining technical expertise with strong communication skills. I am particularly drawn to {company}'s mission and believe my experience aligns well with your needs.

My key strengths include:
• Strong proficiency in {skills[0] if skills else 'relevant technologies'}
• Proven track record of delivering projects on time
• Excellent collaboration and communication abilities
• Passion for continuous learning and improvement

I would welcome the opportunity to discuss how my skills and experience can benefit {company}. Thank you for considering my application.

Best regards,
{name}"""
    
    def _demo_resume_summary(self, profile: Dict, job: Dict) -> str:
        """Generate a demo resume summary"""
        title = job.get("title", "Professional")
        skills = profile.get("skills", [])[:5]
        years = profile.get("experience_years", "several")
        
        return f"""PROFESSIONAL SUMMARY
Results-driven {title} with {years} years of experience in {', '.join(skills[:2]) if skills else 'technology'}. Proven ability to deliver high-impact solutions while collaborating effectively with cross-functional teams. Passionate about innovation and continuous improvement.

KEY ACHIEVEMENTS
• Led projects resulting in significant efficiency improvements
• Collaborated with teams to deliver solutions ahead of schedule
• Implemented best practices that improved code quality and team productivity
• Mentored junior team members and contributed to knowledge sharing

SKILLS TO EMPHASIZE
{', '.join(skills) if skills else 'Relevant technical and soft skills'}"""
