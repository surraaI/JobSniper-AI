"""
Scout Agent - Opportunity Hunter
Scans job boards for matching opportunities using Adzuna API with demo fallback.
"""

import httpx
from typing import Optional, List, Dict, Any
from datetime import datetime

from app.config import settings
from app.services.demo_data import get_demo_jobs


class ScoutAgent:
    """The Scout - discovers job opportunities across multiple sources."""
    
    def __init__(self):
        self.adzuna_base_url = "https://api.adzuna.com/v1/api/jobs"
        self.adzuna_app_id = settings.adzuna_app_id
        self.adzuna_api_key = settings.adzuna_api_key
    
    async def hunt(
        self,
        query: Optional[str] = None,
        location: Optional[str] = None,
        remote_only: bool = False,
        limit: int = 20,
    ) -> List[Dict[str, Any]]:
        """
        Hunt for jobs matching the criteria.
        Falls back to demo data if API unavailable.
        """
        try:
            if not self.adzuna_app_id or not self.adzuna_api_key:
                raise ValueError("Adzuna credentials not configured")
            
            jobs = await self._search_adzuna(query, location, remote_only, limit)
            return jobs
        except Exception as e:
            print(f"[Scout] API error, using demo data: {e}")
            return get_demo_jobs(limit=limit)
    
    async def _search_adzuna(
        self,
        query: Optional[str],
        location: Optional[str],
        remote_only: bool,
        limit: int,
    ) -> List[Dict[str, Any]]:
        """Search Adzuna API for jobs"""
        country = "us"  # Default to US
        
        params = {
            "app_id": self.adzuna_app_id,
            "app_key": self.adzuna_api_key,
            "results_per_page": min(limit, 50),
            "content-type": "application/json",
        }
        
        if query:
            params["what"] = query
        
        if location:
            params["where"] = location
        
        if remote_only:
            params["what"] = f"{params.get('what', '')} remote".strip()
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.adzuna_base_url}/{country}/search/1",
                params=params,
                timeout=10.0,
            )
            response.raise_for_status()
            data = response.json()
        
        jobs = []
        for result in data.get("results", []):
            job = self._normalize_adzuna_job(result)
            jobs.append(job)
        
        return jobs
    
    def _normalize_adzuna_job(self, raw: Dict) -> Dict[str, Any]:
        """Normalize Adzuna job data to our schema"""
        salary_min = None
        salary_max = None
        
        if raw.get("salary_min"):
            salary_min = int(raw["salary_min"])
        if raw.get("salary_max"):
            salary_max = int(raw["salary_max"])
        
        return {
            "external_id": raw.get("id"),
            "source": "adzuna",
            "company": raw.get("company", {}).get("display_name", "Unknown"),
            "title": raw.get("title", ""),
            "description": raw.get("description", ""),
            "location": raw.get("location", {}).get("display_name", ""),
            "salary_min": salary_min,
            "salary_max": salary_max,
            "job_url": raw.get("redirect_url", ""),
            "posted_at": raw.get("created"),
            "job_type": raw.get("contract_type"),
            "remote_type": "remote" if "remote" in raw.get("title", "").lower() else None,
        }
    
    async def search_theirstack(
        self,
        query: Optional[str] = None,
        limit: int = 20,
    ) -> List[Dict[str, Any]]:
        """
        Search TheirStack API for tech jobs.
        Secondary source for startup/tech roles.
        """
        if not settings.theirstack_api_key:
            return []
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    "https://api.theirstack.com/v1/jobs",
                    headers={"Authorization": f"Bearer {settings.theirstack_api_key}"},
                    params={"q": query, "limit": limit},
                    timeout=10.0,
                )
                response.raise_for_status()
                data = response.json()
            
            return [self._normalize_theirstack_job(j) for j in data.get("jobs", [])]
        except Exception as e:
            print(f"[Scout] TheirStack error: {e}")
            return []
    
    def _normalize_theirstack_job(self, raw: Dict) -> Dict[str, Any]:
        """Normalize TheirStack job data"""
        return {
            "external_id": raw.get("id"),
            "source": "theirstack",
            "company": raw.get("company_name", "Unknown"),
            "title": raw.get("title", ""),
            "description": raw.get("description", ""),
            "location": raw.get("location", ""),
            "salary_min": raw.get("salary_min"),
            "salary_max": raw.get("salary_max"),
            "job_url": raw.get("url", ""),
            "posted_at": raw.get("posted_at"),
            "remote_type": raw.get("remote_type"),
        }
