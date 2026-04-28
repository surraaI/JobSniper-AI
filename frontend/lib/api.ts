/**
 * JobSniper AI API Client
 * Handles all communication with the FastAPI backend
 */

const API_BASE = "/api";

interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: string;
}

async function fetchApi<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<ApiResponse<T>> {
  try {
    const response = await fetch(`${API_BASE}${endpoint}`, {
      ...options,
      headers: {
        "Content-Type": "application/json",
        ...options.headers,
      },
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({ message: "Request failed" }));
      return { success: false, error: error.message || error.detail || "Request failed" };
    }

    const data = await response.json();
    return { success: true, data };
  } catch (error) {
    return { success: false, error: "Network error. Please try again." };
  }
}

// Health check
export async function checkHealth() {
  return fetchApi<{ status: string; agents: string[] }>("/health");
}

// Profile APIs
export async function getProfile(userId: string) {
  return fetchApi<{
    id: string;
    full_name: string;
    email: string;
    linkedin_url: string;
    skills: string[];
    experience_years: number;
    preferences: {
      target_roles: string[];
      target_locations: string[];
      remote_preference: string;
      salary_min: number;
      salary_max: number;
    };
    telegram_chat_id: string | null;
  }>(`/profile/${userId}`);
}

export async function updateProfile(userId: string, data: Record<string, unknown>) {
  return fetchApi(`/profile/${userId}`, {
    method: "PUT",
    body: JSON.stringify(data),
  });
}

export async function uploadResume(userId: string, resumeText: string) {
  return fetchApi(`/profile/${userId}/resume`, {
    method: "POST",
    body: JSON.stringify({ resume_text: resumeText }),
  });
}

// Jobs APIs
export async function getJobs(params?: {
  limit?: number;
  offset?: number;
  source?: string;
}) {
  const searchParams = new URLSearchParams();
  if (params?.limit) searchParams.set("limit", params.limit.toString());
  if (params?.offset) searchParams.set("offset", params.offset.toString());
  if (params?.source) searchParams.set("source", params.source);

  return fetchApi<{
    id: string;
    company: string;
    title: string;
    location: string;
    salary_min: number;
    salary_max: number;
    job_url: string;
    source: string;
    posted_at: string;
  }[]>(`/jobs?${searchParams.toString()}`);
}

export async function searchJobs(query: string) {
  return fetchApi(`/jobs/search?q=${encodeURIComponent(query)}`);
}

// Applications APIs
export async function getApplications(userId: string) {
  return fetchApi<{
    id: string;
    job_id: string;
    status: string;
    match_score: number;
    tailored_resume: string | null;
    cover_letter: string | null;
    sentinel_update: string | null;
    deadline: string | null;
    created_at: string;
    jobs: {
      id: string;
      company: string;
      title: string;
      location: string;
      job_url: string;
      salary_min: number;
      salary_max: number;
    };
  }[]>(`/profile/${userId}/applications`);
}

export async function approveApplication(applicationId: string) {
  return fetchApi(`/jobs/applications/${applicationId}/approve`, {
    method: "POST",
  });
}

export async function rejectApplication(applicationId: string) {
  return fetchApi(`/jobs/applications/${applicationId}/reject`, {
    method: "POST",
  });
}

// Agent APIs
export async function triggerScout(userId: string) {
  return fetchApi(`/agents/scout/run`, {
    method: "POST",
    body: JSON.stringify({ user_id: userId }),
  });
}

export async function triggerStrategist(userId: string, jobIds: string[]) {
  return fetchApi(`/agents/strategist/analyze`, {
    method: "POST",
    body: JSON.stringify({ user_id: userId, job_ids: jobIds }),
  });
}

export async function generateCoverLetter(userId: string, jobId: string) {
  return fetchApi<{ cover_letter: string }>(`/agents/ghostwriter/cover-letter`, {
    method: "POST",
    body: JSON.stringify({ user_id: userId, job_id: jobId }),
  });
}

export async function generateOutreach(userId: string, jobId: string) {
  return fetchApi<{ outreach_message: string }>(`/agents/liaison/outreach`, {
    method: "POST",
    body: JSON.stringify({ user_id: userId, job_id: jobId }),
  });
}

export async function getAgentLogs(userId: string) {
  return fetchApi<{
    id: string;
    agent: string;
    action: string;
    created_at: string;
    output_data: Record<string, unknown>;
  }[]>(`/agents/logs/${userId}`);
}

// Telegram APIs
export async function getTelegramStatus(userId: string) {
  return fetchApi<{ connected: boolean; chat_id?: string }>(`/telegram/status/${userId}`);
}

export async function connectTelegram(userId: string, code: string) {
  return fetchApi(`/telegram/connect`, {
    method: "POST",
    body: JSON.stringify({ user_id: userId, code }),
  });
}

export async function sendJobToTelegram(userId: string, jobId: string, matchScore: number) {
  return fetchApi(`/telegram/send-job/${userId}`, {
    method: "POST",
    body: JSON.stringify({ job_id: jobId, match_score: matchScore }),
  });
}
