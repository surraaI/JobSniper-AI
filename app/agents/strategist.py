"""
Strategist Agent - Match Analyzer
Uses GPT-4o to score job-candidate fit and prioritize opportunities.
"""

from typing import Dict, Any
import json

from app.services.openai import get_completion
from app.config import settings


class StrategistAgent:
    """The Strategist - analyzes and scores job matches."""
    
    async def score_match(self, job: Dict[str, Any], profile: Dict[str, Any]) -> int:
        """
        Score how well a job matches the candidate's profile.
        Returns a score from 0-100.
        """
        if settings.demo_mode or not settings.openai_api_key:
            return self._calculate_demo_score(job, profile)
        
        try:
            prompt = self._build_scoring_prompt(job, profile)
            response = await get_completion(prompt, max_tokens=100)
            
            # Extract score from response
            score = self._parse_score(response)
            return score
        except Exception as e:
            print(f"[Strategist] Scoring error: {e}")
            return self._calculate_demo_score(job, profile)
    
    def _build_scoring_prompt(self, job: Dict, profile: Dict) -> str:
        """Build the GPT prompt for job scoring"""
        skills = profile.get("skills", [])
        preferences = profile.get("preferences", {})
        
        return f"""Analyze this job match and return ONLY a score from 0-100.

CANDIDATE PROFILE:
- Skills: {', '.join(skills) if skills else 'Not specified'}
- Experience: {profile.get('experience_years', 'Unknown')} years
- Target Roles: {', '.join(preferences.get('target_roles', []))}
- Target Locations: {', '.join(preferences.get('target_locations', []))}
- Remote Preference: {preferences.get('remote_preference', 'any')}
- Salary Range: ${preferences.get('salary_min', 0):,} - ${preferences.get('salary_max', 999999):,}

JOB POSTING:
- Title: {job.get('title', 'Unknown')}
- Company: {job.get('company', 'Unknown')}
- Location: {job.get('location', 'Unknown')}
- Salary: ${job.get('salary_min', 0):,} - ${job.get('salary_max', 0):,}
- Description: {job.get('description', '')[:500]}

Consider:
1. Skill match (40% weight)
2. Role/title alignment (25% weight)
3. Location/remote fit (15% weight)
4. Salary alignment (10% weight)
5. Company/industry fit (10% weight)

Return ONLY a number from 0-100, nothing else."""
    
    def _parse_score(self, response: str) -> int:
        """Parse score from GPT response"""
        try:
            # Try to extract just the number
            cleaned = ''.join(c for c in response if c.isdigit())
            score = int(cleaned[:3]) if cleaned else 50
            return min(100, max(0, score))
        except:
            return 50
    
    def _calculate_demo_score(self, job: Dict, profile: Dict) -> int:
        """Calculate a demo score based on simple keyword matching"""
        score = 50  # Base score
        
        title = job.get("title", "").lower()
        description = job.get("description", "").lower()
        skills = [s.lower() for s in profile.get("skills", [])]
        preferences = profile.get("preferences", {})
        target_roles = [r.lower() for r in preferences.get("target_roles", [])]
        
        # Skill match bonus
        for skill in skills:
            if skill in title or skill in description:
                score += 5
        
        # Role match bonus
        for role in target_roles:
            if role in title:
                score += 15
        
        # Remote bonus if preferred
        if preferences.get("remote_preference") == "remote":
            if "remote" in title.lower() or "remote" in job.get("location", "").lower():
                score += 10
        
        # Salary alignment
        job_min = job.get("salary_min", 0)
        job_max = job.get("salary_max", 0)
        pref_min = preferences.get("salary_min", 0)
        
        if job_min and pref_min and job_min >= pref_min:
            score += 10
        
        return min(100, max(0, score))
    
    async def analyze_fit(self, job: Dict, profile: Dict) -> Dict[str, Any]:
        """
        Detailed analysis of job fit.
        Returns score, pros, cons, and recommendations.
        """
        score = await self.score_match(job, profile)
        
        pros = []
        cons = []
        
        # Simple analysis
        skills = [s.lower() for s in profile.get("skills", [])]
        title = job.get("title", "").lower()
        
        for skill in skills:
            if skill in title or skill in job.get("description", "").lower():
                pros.append(f"Matches your {skill} skills")
        
        if not pros:
            cons.append("Limited skill overlap in job description")
        
        if "remote" in job.get("location", "").lower():
            pros.append("Remote-friendly position")
        
        return {
            "score": score,
            "pros": pros[:5],
            "cons": cons[:3],
            "recommendation": "Strong match" if score >= 80 else "Good fit" if score >= 60 else "Consider carefully",
        }
