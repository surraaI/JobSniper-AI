const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "https://jobsniper-ai.onrender.com"

// Types
export interface Job {
  id: string
  company: string
  title: string
  location: string
  salary_min?: number
  salary_max?: number
  job_url: string
  description?: string
  posted_at?: string
  source: string
}

export interface Application {
  id: string
  job_id: string
  user_id: string
  status: string
  match_score: number
  tailored_resume?: string
  cover_letter?: string
  sentinel_update?: string
  deadline?: string
  applied_at?: string
  created_at: string
  job?: Job
}

export interface Profile {
  id: string
  full_name?: string
  email?: string
  linkedin_url?: string
  resume_text?: string
  skills?: string[]
  experience_years?: number
  telegram_chat_id?: string
  preferences?: {
    target_roles: string[]
    target_locations: string[]
    remote_preference: string
    salary_min?: number
    salary_max?: number
  }
}

export interface AgentResponse {
  success: boolean
  message: string
  data?: Record<string, unknown>
}

// API Client
class ApiClient {
  private baseUrl: string
  private token: string | null = null

  constructor(baseUrl: string) {
    this.baseUrl = baseUrl
  }

  setToken(token: string) {
    this.token = token
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const headers: HeadersInit = {
      "Content-Type": "application/json",
      ...options.headers,
    }

    if (this.token) {
      headers["Authorization"] = `Bearer ${this.token}`
    }

    const response = await fetch(`${this.baseUrl}${endpoint}`, {
      ...options,
      headers,
    })

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: "Request failed" }))
      throw new Error(error.detail || "Request failed")
    }

    return response.json()
  }

  // Health
  async checkHealth() {
    return this.request<{ status: string; message: string }>("/health")
  }

  // Jobs
  async discoverJobs(query: string, location?: string) {
    const params = new URLSearchParams({ query })
    if (location) params.append("location", location)
    return this.request<{ jobs: Job[]; source: string }>(`/jobs/discover?${params}`)
  }

  async getApplications(status?: string) {
    const params = status ? `?status=${status}` : ""
    return this.request<{ applications: Application[] }>(`/jobs/applications${params}`)
  }

  async approveApplication(applicationId: string) {
    return this.request<Application>(`/jobs/applications/${applicationId}/approve`, {
      method: "POST",
    })
  }

  async rejectApplication(applicationId: string) {
    return this.request<Application>(`/jobs/applications/${applicationId}/reject`, {
      method: "POST",
    })
  }

  // Profile
  async getProfile() {
    return this.request<Profile>("/profile")
  }

  async updateProfile(data: Partial<Profile>) {
    return this.request<Profile>("/profile", {
      method: "PUT",
      body: JSON.stringify(data),
    })
  }

  async updatePreferences(preferences: Profile["preferences"]) {
    return this.request<Profile>("/profile/preferences", {
      method: "PUT",
      body: JSON.stringify(preferences),
    })
  }

  async linkTelegram(chatId: string) {
    return this.request<{ success: boolean }>("/profile/telegram", {
      method: "POST",
      body: JSON.stringify({ chat_id: chatId }),
    })
  }

  // Agents
  async runScout(query: string, location?: string) {
    return this.request<AgentResponse>("/agents/scout/run", {
      method: "POST",
      body: JSON.stringify({ query, location }),
    })
  }

  async runStrategist(jobIds: string[]) {
    return this.request<AgentResponse>("/agents/strategist/run", {
      method: "POST",
      body: JSON.stringify({ job_ids: jobIds }),
    })
  }

  async runGhostwriter(applicationId: string) {
    return this.request<AgentResponse>("/agents/ghostwriter/run", {
      method: "POST",
      body: JSON.stringify({ application_id: applicationId }),
    })
  }

  async runFullPipeline(query: string, location?: string) {
    return this.request<AgentResponse>("/agents/pipeline/run", {
      method: "POST",
      body: JSON.stringify({ query, location }),
    })
  }

  async getAgentLogs(limit = 20) {
    return this.request<{ logs: Array<Record<string, unknown>> }>(`/agents/logs?limit=${limit}`)
  }
}

export const api = new ApiClient(API_BASE_URL)
