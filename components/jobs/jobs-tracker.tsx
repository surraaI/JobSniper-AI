"use client"

import { useState, useEffect } from "react"
import { ExternalLink, Search, Filter, Clock, CheckCircle2, XCircle, MessageSquare, Building2, MapPin, Calendar, FileText, Mail, AlertTriangle, Shield, Loader2, RefreshCw } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Badge } from "@/components/ui/badge"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import { api } from "@/lib/api"

type JobStatus = "applied" | "under_review" | "assessment" | "interview_scheduled" | "interview" | "rejected" | "offer" | "pending_approval" | "approved" | "withdrawn"

interface Job {
  id: string
  company: string
  position: string
  location: string
  salary: string
  appliedDate: string
  status: JobStatus
  jobUrl: string
  matchScore: number
  notes?: string
  sentinelUpdate?: string
  deadline?: string
  source: "sniper" | "sentinel"
}

const mockJobs: Job[] = [
  {
    id: "1",
    company: "Stripe",
    position: "Senior Frontend Engineer",
    location: "San Francisco, CA (Remote)",
    salary: "$180k - $220k",
    appliedDate: "2026-04-26",
    status: "interview_scheduled",
    jobUrl: "https://stripe.com/jobs/listing/senior-frontend-engineer",
    matchScore: 94,
    notes: "Interview scheduled for May 2nd",
    sentinelUpdate: "Calendly link detected - Interview confirmed via email",
    source: "sniper",
  },
  {
    id: "2",
    company: "Bending Spoons",
    position: "Product Intern - Evernote",
    location: "Milan, Italy (Remote)",
    salary: "€40k - €50k",
    appliedDate: "2026-04-25",
    status: "assessment",
    jobUrl: "https://bendingspoons.com/careers/product-intern",
    matchScore: 87,
    sentinelUpdate: "Technical assessment received - BRGHT IQ Test required",
    deadline: "2026-05-01",
    source: "sniper",
  },
  {
    id: "3",
    company: "Vercel",
    position: "Staff Software Engineer",
    location: "Remote",
    salary: "$200k - $250k",
    appliedDate: "2026-04-25",
    status: "under_review",
    jobUrl: "https://vercel.com/careers/staff-software-engineer",
    matchScore: 91,
    sentinelUpdate: "Application viewed by recruiter",
    source: "sniper",
  },
  {
    id: "4",
    company: "Linear",
    position: "Full Stack Developer",
    location: "Remote (US/EU)",
    salary: "$150k - $190k",
    appliedDate: "2026-04-24",
    status: "applied",
    jobUrl: "https://linear.app/careers/full-stack-developer",
    matchScore: 88,
    source: "sniper",
  },
  {
    id: "5",
    company: "Notion",
    position: "Product Engineer",
    location: "New York, NY (Hybrid)",
    salary: "$170k - $210k",
    appliedDate: "2026-04-23",
    status: "interview",
    jobUrl: "https://notion.so/careers/product-engineer",
    matchScore: 86,
    notes: "Completed first round, awaiting feedback",
    sentinelUpdate: "Follow-up email from recruiter detected",
    source: "sniper",
  },
  {
    id: "6",
    company: "Vatemp",
    position: "Full Stack Developer",
    location: "Remote",
    salary: "$120k - $150k",
    appliedDate: "2026-04-22",
    status: "assessment",
    jobUrl: "https://vatemp.com/careers/full-stack-developer",
    matchScore: 84,
    sentinelUpdate: "Technical screening questionnaire received",
    deadline: "2026-04-30",
    source: "sniper",
  },
  {
    id: "7",
    company: "Figma",
    position: "Senior Software Engineer",
    location: "San Francisco, CA",
    salary: "$175k - $225k",
    appliedDate: "2026-04-22",
    status: "rejected",
    jobUrl: "https://figma.com/careers/senior-software-engineer",
    matchScore: 82,
    sentinelUpdate: "Rejection email detected - 2 similar roles found as replacements",
    source: "sniper",
  },
  {
    id: "8",
    company: "Anthropic",
    position: "ML Engineer",
    location: "San Francisco, CA",
    salary: "$250k - $350k",
    appliedDate: "2026-04-21",
    status: "offer",
    jobUrl: "https://anthropic.com/careers/ml-engineer",
    matchScore: 79,
    notes: "Offer received! $280k base + equity",
    sentinelUpdate: "Offer letter detected in inbox",
    source: "sniper",
  },
  {
    id: "9",
    company: "Jobgether",
    position: "Remote Engineer",
    location: "Remote (Global)",
    salary: "$130k - $170k",
    appliedDate: "2026-04-20",
    status: "under_review",
    jobUrl: "https://jobgether.com/careers/remote-engineer",
    matchScore: 85,
    sentinelUpdate: "Status update email - Application under review",
    source: "sniper",
  },
  {
    id: "10",
    company: "Plaid",
    position: "Software Engineer",
    location: "Remote",
    salary: "$160k - $200k",
    appliedDate: "2026-04-19",
    status: "applied",
    jobUrl: "https://plaid.com/careers/software-engineer",
    matchScore: 83,
    source: "sniper",
  },
]

const statusConfig: Record<JobStatus, { label: string; color: string; icon: React.ReactNode }> = {
  applied: {
    label: "Applied",
    color: "bg-secondary text-secondary-foreground",
    icon: <Clock className="h-3.5 w-3.5" />,
  },
  under_review: {
    label: "Under Review",
    color: "bg-blue-500/20 text-blue-400",
    icon: <Mail className="h-3.5 w-3.5" />,
  },
  assessment: {
    label: "Assessment",
    color: "bg-amber-500/20 text-amber-400",
    icon: <FileText className="h-3.5 w-3.5" />,
  },
  interview_scheduled: {
    label: "Interview Scheduled",
    color: "bg-cyan-500/20 text-cyan-400",
    icon: <Calendar className="h-3.5 w-3.5" />,
  },
  interview: {
    label: "In Progress",
    color: "bg-accent/20 text-accent",
    icon: <MessageSquare className="h-3.5 w-3.5" />,
  },
  rejected: {
    label: "Rejected",
    color: "bg-destructive/20 text-destructive",
    icon: <XCircle className="h-3.5 w-3.5" />,
  },
  offer: {
    label: "Offer",
    color: "bg-green-500/20 text-green-400",
    icon: <CheckCircle2 className="h-3.5 w-3.5" />,
  },
}

export function JobsTracker() {
  const [searchQuery, setSearchQuery] = useState("")
  const [statusFilter, setStatusFilter] = useState<string>("all")
  const [jobs, setJobs] = useState<Job[]>(mockJobs)
  const [loading, setLoading] = useState(false)
  const [usingDemo, setUsingDemo] = useState(true)

  const fetchJobs = async () => {
    setLoading(true)
    try {
      const response = await api.getApplications()
      if (response.applications && response.applications.length > 0) {
        const mappedJobs: Job[] = response.applications.map((app) => ({
          id: app.id,
          company: app.job?.company || "Unknown",
          position: app.job?.title || "Unknown Position",
          location: app.job?.location || "Unknown",
          salary: app.job?.salary_min && app.job?.salary_max 
            ? `$${app.job.salary_min / 1000}k - $${app.job.salary_max / 1000}k`
            : "Not specified",
          appliedDate: app.applied_at || app.created_at,
          status: app.status as JobStatus,
          jobUrl: app.job?.job_url || "#",
          matchScore: app.match_score || 0,
          sentinelUpdate: app.sentinel_update,
          deadline: app.deadline,
          source: "sniper" as const,
        }))
        setJobs(mappedJobs)
        setUsingDemo(false)
      }
    } catch (error) {
      console.log("[v0] Using demo data - API unavailable:", error)
      setJobs(mockJobs)
      setUsingDemo(true)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchJobs()
  }, [])

  const filteredJobs = jobs.filter((job) => {
    const matchesSearch =
      job.company.toLowerCase().includes(searchQuery.toLowerCase()) ||
      job.position.toLowerCase().includes(searchQuery.toLowerCase())
    const matchesStatus = statusFilter === "all" || job.status === statusFilter
    return matchesSearch && matchesStatus
  })

  const stats = {
    total: jobs.length,
    interviews: jobs.filter((j) => j.status === "interview" || j.status === "interview_scheduled").length,
    assessments: jobs.filter((j) => j.status === "assessment").length,
    offers: jobs.filter((j) => j.status === "offer").length,
    actionRequired: jobs.filter((j) => j.deadline || j.status === "assessment" || j.status === "interview_scheduled").length,
  }

  return (
    <div className="space-y-6">
      {/* Header with refresh */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          {usingDemo && (
            <Badge variant="outline" className="text-amber-400 border-amber-400/50">
              Demo Mode
            </Badge>
          )}
          {!usingDemo && (
            <Badge variant="outline" className="text-green-400 border-green-400/50">
              Live Data
            </Badge>
          )}
        </div>
        <Button
          variant="outline"
          size="sm"
          onClick={fetchJobs}
          disabled={loading}
        >
          {loading ? (
            <Loader2 className="h-4 w-4 animate-spin" />
          ) : (
            <RefreshCw className="h-4 w-4" />
          )}
          <span className="ml-2">Refresh</span>
        </Button>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
        <div className="rounded-lg border border-border bg-card p-4">
          <p className="text-sm text-muted-foreground">Total Applied</p>
          <p className="text-2xl font-bold">{stats.total}</p>
        </div>
        <div className="rounded-lg border border-amber-500/30 bg-card p-4">
          <div className="flex items-center gap-2">
            <AlertTriangle className="h-4 w-4 text-amber-400" />
            <p className="text-sm text-muted-foreground">Action Required</p>
          </div>
          <p className="text-2xl font-bold text-amber-400">{stats.actionRequired}</p>
        </div>
        <div className="rounded-lg border border-border bg-card p-4">
          <p className="text-sm text-muted-foreground">Assessments</p>
          <p className="text-2xl font-bold text-amber-400">{stats.assessments}</p>
        </div>
        <div className="rounded-lg border border-border bg-card p-4">
          <p className="text-sm text-muted-foreground">Interviews</p>
          <p className="text-2xl font-bold text-accent">{stats.interviews}</p>
        </div>
        <div className="rounded-lg border border-border bg-card p-4">
          <p className="text-sm text-muted-foreground">Offers</p>
          <p className="text-2xl font-bold text-green-400">{stats.offers}</p>
        </div>
      </div>

      {/* Filters */}
      <div className="flex flex-col sm:flex-row gap-4">
        <div className="relative flex-1">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
          <Input
            placeholder="Search by company or position..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="pl-10 bg-card border-border"
          />
        </div>
        <Select value={statusFilter} onValueChange={setStatusFilter}>
          <SelectTrigger className="w-full sm:w-48 bg-card border-border">
            <Filter className="h-4 w-4 mr-2" />
            <SelectValue placeholder="Filter by status" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">All Statuses</SelectItem>
            <SelectItem value="applied">Applied</SelectItem>
            <SelectItem value="under_review">Under Review</SelectItem>
            <SelectItem value="assessment">Assessment</SelectItem>
            <SelectItem value="interview_scheduled">Interview Scheduled</SelectItem>
            <SelectItem value="interview">In Progress</SelectItem>
            <SelectItem value="offer">Offer</SelectItem>
            <SelectItem value="rejected">Rejected</SelectItem>
          </SelectContent>
        </Select>
      </div>

      {/* Jobs List */}
      <div className="space-y-3">
        {filteredJobs.map((job) => (
          <div
            key={job.id}
            className="rounded-lg border border-border bg-card p-4 hover:border-accent/50 transition-colors"
          >
            <div className="flex flex-col lg:flex-row lg:items-center gap-4">
              {/* Company & Position */}
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2 mb-1">
                  <Building2 className="h-4 w-4 text-muted-foreground shrink-0" />
                  <span className="font-medium truncate">{job.company}</span>
                  <Badge variant="outline" className="shrink-0 text-xs">
                    {job.matchScore}% match
                  </Badge>
                </div>
                <h3 className="text-lg font-semibold truncate">{job.position}</h3>
                <div className="flex flex-wrap items-center gap-x-4 gap-y-1 mt-2 text-sm text-muted-foreground">
                  <span className="flex items-center gap-1">
                    <MapPin className="h-3.5 w-3.5" />
                    {job.location}
                  </span>
                  <span className="flex items-center gap-1">
                    <Calendar className="h-3.5 w-3.5" />
                    {new Date(job.appliedDate).toLocaleDateString("en-US", {
                      month: "short",
                      day: "numeric",
                      year: "numeric",
                    })}
                  </span>
                  <span className="font-medium text-foreground">{job.salary}</span>
                </div>
                {job.sentinelUpdate && (
                  <div className="mt-2 flex items-start gap-2 text-sm">
                    <Shield className="h-4 w-4 text-green-500 shrink-0 mt-0.5" />
                    <span className="text-green-400">{job.sentinelUpdate}</span>
                  </div>
                )}
                {job.deadline && (
                  <div className="mt-2 flex items-center gap-2 text-sm">
                    <AlertTriangle className="h-4 w-4 text-amber-400" />
                    <span className="text-amber-400">
                      Deadline: {new Date(job.deadline).toLocaleDateString("en-US", {
                        month: "short",
                        day: "numeric",
                        year: "numeric",
                      })}
                    </span>
                  </div>
                )}
                {job.notes && (
                  <p className="mt-2 text-sm text-muted-foreground">{job.notes}</p>
                )}
              </div>

              {/* Status & Actions */}
              <div className="flex items-center gap-3 lg:flex-col lg:items-end">
                <Badge className={`${statusConfig[job.status].color} flex items-center gap-1.5`}>
                  {statusConfig[job.status].icon}
                  {statusConfig[job.status].label}
                </Badge>
                <Button
                  variant="outline"
                  size="sm"
                  className="shrink-0"
                  asChild
                >
                  <a href={job.jobUrl} target="_blank" rel="noopener noreferrer">
                    <ExternalLink className="h-4 w-4 mr-2" />
                    View Job Post
                  </a>
                </Button>
              </div>
            </div>
          </div>
        ))}

        {filteredJobs.length === 0 && (
          <div className="text-center py-12 text-muted-foreground">
            <p>No jobs found matching your criteria.</p>
          </div>
        )}
      </div>
    </div>
  )
}
