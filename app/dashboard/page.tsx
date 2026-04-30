"use client"

import { useState, useEffect } from "react"
import { useRouter } from "next/navigation"
import { createClient } from "@/lib/supabase/client"
import { api, type Profile, type Application } from "@/lib/api"
import { Header } from "@/components/landing/header"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import { Badge } from "@/components/ui/badge"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import {
  Crosshair,
  Radar,
  Brain,
  PenTool,
  Shield,
  Play,
  Loader2,
  User,
  Briefcase,
  MapPin,
  DollarSign,
  Send,
  CheckCircle,
  AlertTriangle,
} from "lucide-react"

export default function DashboardPage() {
  const [user, setUser] = useState<{ id: string; email: string } | null>(null)
  const [profile, setProfile] = useState<Profile | null>(null)
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [runningAgent, setRunningAgent] = useState<string | null>(null)
  const [agentResult, setAgentResult] = useState<string | null>(null)
  const [searchQuery, setSearchQuery] = useState("")
  const [searchLocation, setSearchLocation] = useState("")
  const router = useRouter()

  // Form state
  const [fullName, setFullName] = useState("")
  const [linkedinUrl, setLinkedinUrl] = useState("")
  const [resumeText, setResumeText] = useState("")
  const [skills, setSkills] = useState("")
  const [targetRoles, setTargetRoles] = useState("")
  const [targetLocations, setTargetLocations] = useState("")
  const [salaryMin, setSalaryMin] = useState("")
  const [salaryMax, setSalaryMax] = useState("")
  const [telegramChatId, setTelegramChatId] = useState("")

  useEffect(() => {
    const checkAuth = async () => {
      const supabase = createClient()
      const { data: { user } } = await supabase.auth.getUser()
      
      if (!user) {
        router.push("/auth/login")
        return
      }

      setUser({ id: user.id, email: user.email || "" })
      
      // Load profile from Supabase directly
      const { data: profileData } = await supabase
        .from("profiles")
        .select("*")
        .eq("id", user.id)
        .single()

      if (profileData) {
        setProfile(profileData)
        setFullName(profileData.full_name || "")
        setLinkedinUrl(profileData.linkedin_url || "")
        setResumeText(profileData.resume_text || "")
        setSkills(profileData.skills?.join(", ") || "")
        setTelegramChatId(profileData.telegram_chat_id || "")
        if (profileData.preferences) {
          setTargetRoles(profileData.preferences.target_roles?.join(", ") || "")
          setTargetLocations(profileData.preferences.target_locations?.join(", ") || "")
          setSalaryMin(profileData.preferences.salary_min?.toString() || "")
          setSalaryMax(profileData.preferences.salary_max?.toString() || "")
        }
      }
      
      setLoading(false)
    }

    checkAuth()
  }, [router])

  const handleSaveProfile = async () => {
    if (!user) return
    setSaving(true)

    const supabase = createClient()
    const { error } = await supabase
      .from("profiles")
      .upsert({
        id: user.id,
        full_name: fullName,
        linkedin_url: linkedinUrl,
        resume_text: resumeText,
        skills: skills.split(",").map(s => s.trim()).filter(Boolean),
        telegram_chat_id: telegramChatId || null,
        preferences: {
          target_roles: targetRoles.split(",").map(s => s.trim()).filter(Boolean),
          target_locations: targetLocations.split(",").map(s => s.trim()).filter(Boolean),
          salary_min: salaryMin ? parseInt(salaryMin) : null,
          salary_max: salaryMax ? parseInt(salaryMax) : null,
          remote_preference: "any",
        },
        updated_at: new Date().toISOString(),
      })

    setSaving(false)
    if (!error) {
      setAgentResult("Profile saved successfully!")
      setTimeout(() => setAgentResult(null), 3000)
    }
  }

  const runScout = async () => {
    if (!searchQuery) return
    setRunningAgent("scout")
    setAgentResult(null)

    try {
      const result = await api.runScout(searchQuery, searchLocation || undefined)
      setAgentResult(result.message)
    } catch (error) {
      setAgentResult(`Error: ${error instanceof Error ? error.message : "Failed to run Scout"}`)
    } finally {
      setRunningAgent(null)
    }
  }

  const runFullPipeline = async () => {
    if (!searchQuery) return
    setRunningAgent("pipeline")
    setAgentResult(null)

    try {
      const result = await api.runFullPipeline(searchQuery, searchLocation || undefined)
      setAgentResult(result.message)
    } catch (error) {
      setAgentResult(`Error: ${error instanceof Error ? error.message : "Failed to run pipeline"}`)
    } finally {
      setRunningAgent(null)
    }
  }

  const handleLogout = async () => {
    const supabase = createClient()
    await supabase.auth.signOut()
    router.push("/")
  }

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-background">
        <Loader2 className="w-8 h-8 animate-spin text-accent" />
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-background text-foreground">
      <Header />
      <main className="pt-24 pb-16">
        <div className="container mx-auto px-4 max-w-5xl">
          <div className="flex items-center justify-between mb-8">
            <div>
              <h1 className="text-3xl font-bold mb-2">War Room</h1>
              <p className="text-muted-foreground">
                Welcome back, {fullName || user?.email}
              </p>
            </div>
            <Button variant="outline" onClick={handleLogout}>
              Sign out
            </Button>
          </div>

          {agentResult && (
            <div className={`mb-6 p-4 rounded-lg flex items-center gap-3 ${
              agentResult.startsWith("Error") 
                ? "bg-destructive/10 text-destructive" 
                : "bg-green-500/10 text-green-400"
            }`}>
              {agentResult.startsWith("Error") ? (
                <AlertTriangle className="w-5 h-5" />
              ) : (
                <CheckCircle className="w-5 h-5" />
              )}
              {agentResult}
            </div>
          )}

          <Tabs defaultValue="hunt" className="space-y-6">
            <TabsList className="bg-card border border-border">
              <TabsTrigger value="hunt" className="gap-2">
                <Crosshair className="w-4 h-4" />
                Hunt Jobs
              </TabsTrigger>
              <TabsTrigger value="profile" className="gap-2">
                <User className="w-4 h-4" />
                Profile
              </TabsTrigger>
              <TabsTrigger value="preferences" className="gap-2">
                <Briefcase className="w-4 h-4" />
                Preferences
              </TabsTrigger>
            </TabsList>

            <TabsContent value="hunt" className="space-y-6">
              {/* Job Search */}
              <div className="rounded-lg border border-border bg-card p-6">
                <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
                  <Radar className="w-5 h-5 text-accent" />
                  Activate Sniper Mode
                </h2>
                <div className="grid md:grid-cols-2 gap-4 mb-4">
                  <div className="space-y-2">
                    <Label>Job Title / Keywords</Label>
                    <Input
                      placeholder="e.g. Senior Frontend Engineer"
                      value={searchQuery}
                      onChange={(e) => setSearchQuery(e.target.value)}
                      className="bg-secondary border-border"
                    />
                  </div>
                  <div className="space-y-2">
                    <Label>Location (optional)</Label>
                    <Input
                      placeholder="e.g. San Francisco, Remote"
                      value={searchLocation}
                      onChange={(e) => setSearchLocation(e.target.value)}
                      className="bg-secondary border-border"
                    />
                  </div>
                </div>
                <div className="flex flex-wrap gap-3">
                  <Button
                    onClick={runScout}
                    disabled={!searchQuery || runningAgent !== null}
                  >
                    {runningAgent === "scout" ? (
                      <>
                        <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                        Scouting...
                      </>
                    ) : (
                      <>
                        <Radar className="mr-2 h-4 w-4" />
                        Run Scout Only
                      </>
                    )}
                  </Button>
                  <Button
                    variant="default"
                    onClick={runFullPipeline}
                    disabled={!searchQuery || runningAgent !== null}
                    className="bg-accent hover:bg-accent/90"
                  >
                    {runningAgent === "pipeline" ? (
                      <>
                        <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                        Running Pipeline...
                      </>
                    ) : (
                      <>
                        <Play className="mr-2 h-4 w-4" />
                        Full Pipeline (Scout + Strategist + Ghostwriter)
                      </>
                    )}
                  </Button>
                </div>
              </div>

              {/* Agent Status */}
              <div className="grid md:grid-cols-4 gap-4">
                {[
                  { name: "Scout", icon: Radar, desc: "Finding opportunities" },
                  { name: "Strategist", icon: Brain, desc: "Scoring matches" },
                  { name: "Ghostwriter", icon: PenTool, desc: "Crafting applications" },
                  { name: "Sentinel", icon: Shield, desc: "Monitoring inbox" },
                ].map((agent) => (
                  <div
                    key={agent.name}
                    className="rounded-lg border border-border bg-card p-4"
                  >
                    <div className="flex items-center gap-3 mb-2">
                      <div className="p-2 rounded-lg bg-accent/10 text-accent">
                        <agent.icon className="w-4 h-4" />
                      </div>
                      <span className="font-medium">{agent.name}</span>
                    </div>
                    <p className="text-sm text-muted-foreground">{agent.desc}</p>
                    <Badge variant="outline" className="mt-2 text-xs">
                      Ready
                    </Badge>
                  </div>
                ))}
              </div>
            </TabsContent>

            <TabsContent value="profile" className="space-y-6">
              <div className="rounded-lg border border-border bg-card p-6">
                <h2 className="text-xl font-semibold mb-4">Your Profile</h2>
                <div className="space-y-4">
                  <div className="space-y-2">
                    <Label>Full Name</Label>
                    <Input
                      value={fullName}
                      onChange={(e) => setFullName(e.target.value)}
                      placeholder="John Doe"
                      className="bg-secondary border-border"
                    />
                  </div>
                  <div className="space-y-2">
                    <Label>LinkedIn URL</Label>
                    <Input
                      value={linkedinUrl}
                      onChange={(e) => setLinkedinUrl(e.target.value)}
                      placeholder="https://linkedin.com/in/yourprofile"
                      className="bg-secondary border-border"
                    />
                  </div>
                  <div className="space-y-2">
                    <Label>Skills (comma-separated)</Label>
                    <Input
                      value={skills}
                      onChange={(e) => setSkills(e.target.value)}
                      placeholder="React, TypeScript, Node.js, Python"
                      className="bg-secondary border-border"
                    />
                  </div>
                  <div className="space-y-2">
                    <Label>Resume / Experience Summary</Label>
                    <Textarea
                      value={resumeText}
                      onChange={(e) => setResumeText(e.target.value)}
                      placeholder="Paste your resume text or write a summary of your experience..."
                      rows={6}
                      className="bg-secondary border-border"
                    />
                  </div>
                  <div className="space-y-2">
                    <Label>Telegram Chat ID (for notifications)</Label>
                    <Input
                      value={telegramChatId}
                      onChange={(e) => setTelegramChatId(e.target.value)}
                      placeholder="Your Telegram chat ID"
                      className="bg-secondary border-border"
                    />
                    <p className="text-xs text-muted-foreground">
                      Message @JobSniperBot on Telegram to get your chat ID
                    </p>
                  </div>
                </div>
              </div>
            </TabsContent>

            <TabsContent value="preferences" className="space-y-6">
              <div className="rounded-lg border border-border bg-card p-6">
                <h2 className="text-xl font-semibold mb-4">Job Preferences</h2>
                <div className="space-y-4">
                  <div className="space-y-2">
                    <Label className="flex items-center gap-2">
                      <Briefcase className="w-4 h-4" />
                      Target Roles (comma-separated)
                    </Label>
                    <Input
                      value={targetRoles}
                      onChange={(e) => setTargetRoles(e.target.value)}
                      placeholder="Frontend Engineer, Full Stack Developer, Software Engineer"
                      className="bg-secondary border-border"
                    />
                  </div>
                  <div className="space-y-2">
                    <Label className="flex items-center gap-2">
                      <MapPin className="w-4 h-4" />
                      Target Locations (comma-separated)
                    </Label>
                    <Input
                      value={targetLocations}
                      onChange={(e) => setTargetLocations(e.target.value)}
                      placeholder="San Francisco, New York, Remote"
                      className="bg-secondary border-border"
                    />
                  </div>
                  <div className="grid md:grid-cols-2 gap-4">
                    <div className="space-y-2">
                      <Label className="flex items-center gap-2">
                        <DollarSign className="w-4 h-4" />
                        Minimum Salary
                      </Label>
                      <Input
                        type="number"
                        value={salaryMin}
                        onChange={(e) => setSalaryMin(e.target.value)}
                        placeholder="100000"
                        className="bg-secondary border-border"
                      />
                    </div>
                    <div className="space-y-2">
                      <Label className="flex items-center gap-2">
                        <DollarSign className="w-4 h-4" />
                        Maximum Salary
                      </Label>
                      <Input
                        type="number"
                        value={salaryMax}
                        onChange={(e) => setSalaryMax(e.target.value)}
                        placeholder="200000"
                        className="bg-secondary border-border"
                      />
                    </div>
                  </div>
                </div>
              </div>
            </TabsContent>
          </Tabs>

          <div className="mt-6 flex justify-end">
            <Button onClick={handleSaveProfile} disabled={saving}>
              {saving ? (
                <>
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                  Saving...
                </>
              ) : (
                <>
                  <Send className="mr-2 h-4 w-4" />
                  Save Profile
                </>
              )}
            </Button>
          </div>
        </div>
      </main>
    </div>
  )
}
