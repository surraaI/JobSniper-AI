"""Supabase client service"""

import os
from supabase import acreate_client, AsyncClient

_client: AsyncClient = None


async def get_client() -> AsyncClient:
    """Get or create async Supabase client"""
    global _client
    
    if _client is None:
        url = os.environ.get("SUPABASE_URL", "")
        key = os.environ.get("SUPABASE_ANON_KEY", "")
        
        if not url or not key:
            raise ValueError("SUPABASE_URL and SUPABASE_ANON_KEY must be set")
        
        _client = await acreate_client(url, key)
    
    return _client


async def get_service_client() -> AsyncClient:
    """Get Supabase client with service role (bypasses RLS)"""
    url = os.environ.get("SUPABASE_URL", "")
    key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY", "")
    
    if not url or not key:
        raise ValueError("Service role key not configured")
    
    return await acreate_client(url, key)
