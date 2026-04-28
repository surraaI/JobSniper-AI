"""
Strategist Agent - Job Matching & Scoring
Analyzes jobs against user profile to calculate match scores.
"""
from typing import Optional
from openai import AsyncOpenAI

from app.config import get_settings


class StrategistAgent:
    """
    The Strategist Agent analyzes discovered jobs and scores them
    based on fit with user's profile, skills, and preferences.
    
    Uses GPT-4o for nuanced matching that goes beyond keyword matching.
    """
    
    def __init__(self):
        self.settings = get_settings()
        self.client = AsyncOpenAI(api_key=self.settings.openai_api_key) if self.settings.openai_api_key else None
    
    async def score_job(
        self,
        job: dict,
        user_profile: dict
    ) -> dict:
        """
        Score a job based on match with user profile.
        Returns job with added match_score and match_reasons.
        """
        if not self.client:
            # Fallback: basic keyword matching
            return self._basic_score(job, user_profile)
        
        try:
            score_data = await self._gpt_score(job, user_profile)
            job["match_score"] = score_data["score"]
            job["match_reasons"] = score_data["reasons"]
            job["concerns"] = score_data.get("concerns", [])
            return job
        except Exception as e:
            print(f"GPT scoring failed: {e}")
            return self._basic_score(job, user_profile)
    
    async def _gpt_score(self, job: dict, user_profile: dict) -> dict:
        """
        Use GPT-4o to score job match.
        """
        system_prompt = """You are a career strategist AI. Your job is to analyze how well a job posting matches a candidate's profile.

Score on a scale of 0-100 where:
- 90-100: Excellent match, should definitely apply
- 75-89: Good match, worth applying
- 60-74: Moderate match, consider applying
- Below 60: Poor match, likely not worth pursuing

Respond in JSON format:
{
    "score": <number>,
    "reasons": ["reason 1", "reason 2", ...],
    "concerns": ["concern 1", "concern 2", ...]
}"""

        user_prompt = f"""
Job Posting:
- Company: {job.get('company', 'Unknown')}
- Position: {job.get('position', 'Unknown')}
- Location: {job.get('location', 'Unknown')}
- Salary: {job.get('salary', 'Not specified')}
- Description: {job.get('description', 'No description')[:1000]}

Candidate Profile:
- Skills: {', '.join(user_profile.get('skills', []))}
- Experience: {user_profile.get('experience_years', 'Unknown')} years
- Target Roles: {', '.join(user_profile.get('preferences', {}).get('target_roles', []))}
- Location Preference: {', '.join(user_profile.get('preferences', {}).get('target_locations', []))}
- Remote Preference: {user_profile.get('preferences', {}).get('remote_preference', 'any')}
- Salary Range: ${user_profile.get('preferences', {}).get('salary_min', 0):,} - ${user_profile.get('preferences', {}).get('salary_max', 0):,}

Analyze the match and provide your assessment in JSON format."""

        response = await self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.3
        )
        
        import json
        return json.loads(response.choices[0].message.content)
    
    def _basic_score(self, job: dict, user_profile: dict) -> dict:
        """
        Fallback: Basic keyword-based scoring.
        """
        score = 50  # Base score
        reasons = []
        
        job_text = f"{job.get('position', '')} {job.get('description', '')}".lower()
        
        # Check skill matches
        skills = user_profile.get("skills", [])
        matched_skills = [s for s in skills if s.lower() in job_text]
        if matched_skills:
            score += min(len(matched_skills) * 5, 25)
            reasons.append(f"Matches skills: {', '.join(matched_skills[:3])}")
        
        # Check role match
        target_roles = user_profile.get("preferences", {}).get("target_roles", [])
        for role in target_roles:
            if role.lower() in job_text:
                score += 15
                reasons.append(f"Matches target role: {role}")
                break
        
        # Check location/remote
        location = job.get("location", "").lower()
        remote_pref = user_profile.get("preferences", {}).get("remote_preference", "any")
        if remote_pref == "remote_only" and "remote" in location:
            score += 10
            reasons.append("Remote position matches preference")
        
        job["match_score"] = min(score, 100)
        job["match_reasons"] = reasons if reasons else ["Basic match based on keywords"]
        return job
    
    async def rank_jobs(
        self,
        jobs: list[dict],
        user_profile: dict
    ) -> list[dict]:
        """
        Score and rank a list of jobs.
        Returns jobs sorted by match_score (highest first).
        """
        scored_jobs = []
        for job in jobs:
            scored_job = await self.score_job(job, user_profile)
            scored_jobs.append(scored_job)
        
        # Sort by match score descending
        scored_jobs.sort(key=lambda x: x.get("match_score", 0), reverse=True)
        return scored_jobs
