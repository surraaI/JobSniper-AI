-- JobSniper AI - Jobs Table
-- Stores discovered job opportunities

CREATE TYPE job_source AS ENUM (
  'adzuna',
  'theirstack',
  'linkedin',
  'upwork',
  'demo'
);

CREATE TABLE IF NOT EXISTS public.jobs (
  id TEXT PRIMARY KEY,
  company TEXT NOT NULL,
  position TEXT NOT NULL,
  location TEXT,
  salary TEXT,
  description TEXT,
  url TEXT NOT NULL,
  source job_source NOT NULL DEFAULT 'demo',
  
  -- Metadata
  discovered_at TIMESTAMPTZ DEFAULT NOW(),
  expires_at TIMESTAMPTZ,
  
  -- Deduplication
  url_hash TEXT UNIQUE,
  
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Index for fast lookups
CREATE INDEX IF NOT EXISTS jobs_company_idx ON public.jobs(company);
CREATE INDEX IF NOT EXISTS jobs_source_idx ON public.jobs(source);
CREATE INDEX IF NOT EXISTS jobs_discovered_at_idx ON public.jobs(discovered_at DESC);

-- No RLS on jobs table - jobs are shared across users
-- Access control is via applications table
