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
import { createClient } from "@/lib/supabase/client"

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

export function JobsTracker() {
  const [jobs, setJobs] = useState<Job[]>([])
  const [filteredJobs, setFilteredJobs] = useState<Job[]>([])
  const [loading, setLoading] = useState(true)
  const [searchQuery, setSearchQuery] = useState("")
  const [statusFilter, setStatusFilter] = useState<JobStatus | "all">("all")
  const [sourceFilter, setSourceFilter] = useState<"all" | "sniper" | "sentinel">("all")

  useEffect(() => {
    const fetchApplications = async () => {
      try {
        setLoading(true)
        const supabase = createClient()
        const { data: { user } } = await supabase.auth.getUser()
        
        if (!user) {
          setLoading(false)
          return
        }

        // Fetch applications with job details
        const { data, error } = await supabase
          .from("applications")
          .select(`
            id,
            status,
            match_score,
            created_at,
            jobs:job_id (
              id,
              title,
              company,
              location,
              salary_min,
              salary_max,
              job_url,
              source
            )
          `)
          .eq("user_id", user.id)
          .order("created_at", { ascending: false })

        if (error) {
          console.error("[v0] Error fetching applications:", error)
          setLoading(false)
          return
        }

        // Transform data to match Job interface
        const transformedJobs: Job[] = (data || []).map((app: any) => {
          const job = app.jobs
          const salaryRange = job.salary_min && job.salary_max 
            ? `$${(job.salary_min / 1000).toFixed(0)}k - $${(job.salary_max / 1000).toFixed(0)}k`
            : "Salary not specified"

          return {
            id: app.id,
            company: job.company || "Unknown Company",
            position: job.title || "Position",
            location: job.location || "Location not specified",
            salary: salaryRange,
            appliedDate: new Date(app.created_at).toISOString().split("T")[0],
            status: app.status || "applied",
            jobUrl: job.job_url || "#",
            matchScore: app.match_score || 0,
            source: job.source === "adzuna" ? "sniper" : "sentinel",
          }
        })

        setJobs(transformedJobs)
        setFilteredJobs(transformedJobs)
      } catch (err) {
        console.error("[v0] Error loading applications:", err)
      } finally {
        setLoading(false)
      }
    }

    fetchApplications()
  }, [])

  // Apply filters
  useEffect(() => {
    let filtered = [...jobs]

    // Search filter
    if (searchQuery.trim()) {
      const query = searchQuery.toLowerCase()
      filtered = filtered.filter(
        (job) =>
          job.company.toLowerCase().includes(query) ||
          job.position.toLowerCase().includes(query)
      )
    }

    // Status filter
    if (statusFilter !== "all") {
      filtered = filtered.filter((job) => job.status === statusFilter)
    }

    // Source filter
    if (sourceFilter !== "all") {
      filtered = filtered.filter((job) => job.source === sourceFilter)
    }

    setFilteredJobs(filtered)
  }, [jobs, searchQuery, statusFilter, sourceFilter])

  if (loading) {
    return (
      <div className="flex items-center justify-center py-12">
        <Loader2 className="w-8 h-8 animate-spin text-accent" />
      </div>
    )
  }

  if (jobs.length === 0) {
    return (
      <div className="text-center py-12">
        <Building2 className="w-12 h-12 mx-auto mb-4 text-muted-foreground" />
        <h3 className="text-lg font-semibold mb-2">No applications yet</h3>
        <p className="text-muted-foreground mb-6">Start hunting for jobs in your dashboard to see applications here</p>
        <Button asChild>
          <a href="/dashboard">Go to Dashboard</a>
        </Button>
      </div>
    )
  }

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
    pending_approval: {
      label: "Pending Approval",
      color: "bg-yellow-500/20 text-yellow-400",
      icon: <Clock className="h-3.5 w-3.5" />,
    },
    approved: {
      label: "Approved",
      color: "bg-emerald-500/20 text-emerald-400",
      icon: <CheckCircle2 className="h-3.5 w-3.5" />,
    },
    withdrawn: {
      label: "Withdrawn",
      color: "bg-slate-500/20 text-slate-300",
      icon: <XCircle className="h-3.5 w-3.5" />,
    },
  }

  const stats = {
    total: jobs.length,
    interviews: jobs.filter((j) => j.status === "interview" || j.status === "interview_scheduled").length,
    assessments: jobs.filter((j) => j.status === "assessment").length,
    offers: jobs.filter((j) => j.status === "offer").length,
    actionRequired: jobs.filter((j) => j.status === "assessment" || j.status === "interview_scheduled").length,
  }

  return (
    <div className="space-y-6">
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
        <Select value={statusFilter as string} onValueChange={(value) => setStatusFilter(value as JobStatus | "all")}>
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
            <SelectItem value="pending_approval">Pending Approval</SelectItem>
            <SelectItem value="approved">Approved</SelectItem>
            <SelectItem value="withdrawn">Withdrawn</SelectItem>
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
