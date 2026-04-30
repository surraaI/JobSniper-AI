"""OpenAI service for GPT-4o completions"""

from openai import AsyncOpenAI
from typing import Optional, Dict, Any, List

from app.config import settings

_client: AsyncOpenAI = None


def get_openai_client() -> AsyncOpenAI:
    """Get or create OpenAI client"""
    global _client
    
    if _client is None:
        if not settings.openai_api_key:
            raise ValueError("OPENAI_API_KEY not configured")
        _client = AsyncOpenAI(api_key=settings.openai_api_key)
    
    return _client


async def get_completion(
    prompt: str,
    model: str = "gpt-4o",
    max_tokens: int = 500,
    temperature: float = 0.7,
) -> str:
    """Get a completion from GPT-4o"""
    client = get_openai_client()
    
    response = await client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=max_tokens,
        temperature=temperature,
    )
    
    return response.choices[0].message.content


async def extract_resume_data(resume_text: str) -> Dict[str, Any]:
    """Extract structured data from resume text"""
    prompt = f"""Analyze this resume and extract:
1. skills (list of technical and soft skills)
2. experience_years (estimated total years)
3. job_titles (list of past titles)
4. education (highest degree)

RESUME:
{resume_text[:3000]}

Return as JSON with keys: skills, experience_years, job_titles, education"""

    client = get_openai_client()
    
    response = await client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500,
        response_format={"type": "json_object"},
    )
    
    import json
    try:
        return json.loads(response.choices[0].message.content)
    except:
        return {"skills": [], "experience_years": None}
