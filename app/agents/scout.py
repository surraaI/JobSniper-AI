"""
Scout Agent - Job Discovery
Scans multiple job sources to find opportunities matching user preferences.
"""
import httpx
from typing import Optional
from datetime import datetime
import hashlib

from app.config import get_settings
from app.services.demo_data import get_demo_jobs


class ScoutAgent:
    """
    The Scout Agent continuously scans job boards and APIs
    to discover new opportunities.
    
    Sources:
    - Adzuna API (primary - real-time job data)
    - TheirStack API (tech company jobs)
    - Fallback: Demo data for hackathon safety
    """
    
    def __init__(self):
        self.settings = get_settings()
        self.client = httpx.AsyncClient(timeout=30.0)
    
    async def discover(
        self,
        keywords: str,
        location: Optional[str] = None,
        remote: bool = True,
        limit: int = 20
    ) -> list[dict]:
        """
        Discover jobs from all configured sources.
        Uses fallback to demo data if APIs fail.
        """
        all_jobs = []
        
        # Try Adzuna first
        try:
            adzuna_jobs = await self._search_adzuna(keywords, location, remote, limit)
            all_jobs.extend(adzuna_jobs)
        except Exception as e:
            print(f"Adzuna API failed: {e}")
        
        # Try TheirStack
        try:
            theirstack_jobs = await self._search_theirstack(keywords, limit)
            all_jobs.extend(theirstack_jobs)
        except Exception as e:
            print(f"TheirStack API failed: {e}")
        
        # If no jobs found, use demo data
        if not all_jobs:
            all_jobs = get_demo_jobs(keywords=keywords, limit=limit)
        
        # Deduplicate by job URL
        seen_urls = set()
        unique_jobs = []
        for job in all_jobs:
            if job["url"] not in seen_urls:
                seen_urls.add(job["url"])
                unique_jobs.append(job)
        
        return unique_jobs[:limit]
    
    async def _search_adzuna(
        self,
        keywords: str,
        location: Optional[str],
        remote: bool,
        limit: int
    ) -> list[dict]:
        """
        Search Adzuna API for jobs.
        https://developer.adzuna.com/
        """
        if not self.settings.adzuna_app_id or not self.settings.adzuna_api_key:
            raise ValueError("Adzuna credentials not configured")
        
        # Build query
        what = keywords
        if remote:
            what += " remote"
        
        params = {
            "app_id": self.settings.adzuna_app_id,
            "app_key": self.settings.adzuna_api_key,
            "results_per_page": limit,
            "what": what,
            "content-type": "application/json"
        }
        
        if location:
            params["where"] = location
        
        # Adzuna US endpoint
        url = "https://api.adzuna.com/v1/api/jobs/us/search/1"
        
        response = await self.client.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        jobs = []
        for item in data.get("results", []):
            job_id = hashlib.md5(item["redirect_url"].encode()).hexdigest()[:12]
            jobs.append({
                "id": f"adzuna_{job_id}",
                "company": item.get("company", {}).get("display_name", "Unknown"),
                "position": item.get("title", "Unknown Position"),
                "location": item.get("location", {}).get("display_name", "Unknown"),
                "salary": self._format_salary(
                    item.get("salary_min"),
                    item.get("salary_max")
                ),
                "description": item.get("description", "")[:500],
                "url": item.get("redirect_url", ""),
                "source": "adzuna",
                "discovered_at": datetime.utcnow().isoformat(),
                "status": "discovered"
            })
        
        return jobs
    
    async def _search_theirstack(
        self,
        keywords: str,
        limit: int
    ) -> list[dict]:
        """
        Search TheirStack API for tech company jobs.
        https://theirstack.com/
        """
        if not self.settings.theirstack_api_key:
            raise ValueError("TheirStack API key not configured")
        
        headers = {
            "Authorization": f"Bearer {self.settings.theirstack_api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "job_title_or": [keywords],
            "limit": limit,
            "posted_at_max_age_days": 7
        }
        
        url = "https://api.theirstack.com/v1/jobs/search"
        
        response = await self.client.post(url, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        jobs = []
        for item in data.get("data", []):
            job_id = hashlib.md5(item.get("url", "").encode()).hexdigest()[:12]
            jobs.append({
                "id": f"theirstack_{job_id}",
                "company": item.get("company_name", "Unknown"),
                "position": item.get("job_title", "Unknown Position"),
                "location": item.get("location", "Remote"),
                "salary": item.get("salary_string", None),
                "description": item.get("description", "")[:500],
                "url": item.get("url", ""),
                "source": "theirstack",
                "discovered_at": datetime.utcnow().isoformat(),
                "status": "discovered"
            })
        
        return jobs
    
    def _format_salary(self, min_salary: Optional[int], max_salary: Optional[int]) -> Optional[str]:
        """Format salary range as string."""
        if not min_salary and not max_salary:
            return None
        
        if min_salary and max_salary:
            return f"${min_salary:,} - ${max_salary:,}"
        elif min_salary:
            return f"${min_salary:,}+"
        else:
            return f"Up to ${max_salary:,}"
    
    async def close(self):
        await self.client.aclose()
