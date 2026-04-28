-- JobSniper AI - Agent Logs Table
-- Tracks all agent activities for debugging and analytics

CREATE TYPE agent_type AS ENUM (
  'scout',
  'strategist',
  'ghostwriter',
  'liaison',
  'sentinel'
);

CREATE TYPE log_level AS ENUM (
  'info',
  'warning',
  'error',
  'success'
);

CREATE TABLE IF NOT EXISTS public.agent_logs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
  
  -- Agent info
  agent agent_type NOT NULL,
  action TEXT NOT NULL,
  level log_level NOT NULL DEFAULT 'info',
  
  -- Details
  message TEXT,
  details JSONB DEFAULT '{}',
  
  -- Related entities
  job_id TEXT REFERENCES public.jobs(id) ON DELETE SET NULL,
  application_id UUID REFERENCES public.applications(id) ON DELETE SET NULL,
  
  -- Timing
  duration_ms INTEGER,
  
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Enable RLS
ALTER TABLE public.agent_logs ENABLE ROW LEVEL SECURITY;

-- RLS Policies - users can only see their own logs
CREATE POLICY "agent_logs_select_own" ON public.agent_logs 
  FOR SELECT USING (auth.uid() = user_id OR user_id IS NULL);

CREATE POLICY "agent_logs_insert_own" ON public.agent_logs 
  FOR INSERT WITH CHECK (auth.uid() = user_id OR user_id IS NULL);

-- Indexes for efficient querying
CREATE INDEX IF NOT EXISTS agent_logs_user_id_idx ON public.agent_logs(user_id);
CREATE INDEX IF NOT EXISTS agent_logs_agent_idx ON public.agent_logs(agent);
CREATE INDEX IF NOT EXISTS agent_logs_created_at_idx ON public.agent_logs(created_at DESC);
CREATE INDEX IF NOT EXISTS agent_logs_level_idx ON public.agent_logs(level);

-- Partition by time for better performance (optional for larger deployments)
-- Can add partitioning later if needed
