"use client"

import { useState } from "react"
import { useRouter } from "next/navigation"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Crosshair, Loader2, X, Plus, ArrowRight, ArrowLeft } from "lucide-react"
import Link from "next/link"
import { api } from "@/lib/api"
import { createClient } from "@/lib/supabase/client"

export default function ProfileSetupPage() {
  const router = useRouter()
  const [step, setStep] = useState(1)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  
  // Step 1: Basic Info
  const [fullName, setFullName] = useState("")
  const [linkedinUrl, setLinkedinUrl] = useState("")
  
  // Step 2: Resume
  const [resumeText, setResumeText] = useState("")
  
  // Step 3: Skills
  const [skills, setSkills] = useState<string[]>([])
  const [newSkill, setNewSkill] = useState("")
  const [experienceYears, setExperienceYears] = useState("")
  
  // Step 4: Preferences
  const [targetRoles, setTargetRoles] = useState<string[]>([])
  const [newRole, setNewRole] = useState("")
  const [targetLocations, setTargetLocations] = useState<string[]>([])
  const [newLocation, setNewLocation] = useState("")
  const [remotePreference, setRemotePreference] = useState("any")
  const [salaryMin, setSalaryMin] = useState("")
  const [salaryMax, setSalaryMax] = useState("")

  const addSkill = () => {
    if (newSkill.trim() && !skills.includes(newSkill.trim())) {
      setSkills([...skills, newSkill.trim()])
      setNewSkill("")
    }
  }

  const removeSkill = (skill: string) => {
    setSkills(skills.filter(s => s !== skill))
  }

  const addRole = () => {
    if (newRole.trim() && !targetRoles.includes(newRole.trim())) {
      setTargetRoles([...targetRoles, newRole.trim()])
      setNewRole("")
    }
  }

  const removeRole = (role: string) => {
    setTargetRoles(targetRoles.filter(r => r !== role))
  }

  const addLocation = () => {
    if (newLocation.trim() && !targetLocations.includes(newLocation.trim())) {
      setTargetLocations([...targetLocations, newLocation.trim()])
      setNewLocation("")
    }
  }

  const removeLocation = (location: string) => {
    setTargetLocations(targetLocations.filter(l => l !== location))
  }

  const handleSubmit = async () => {
    setLoading(true)
    setError(null)

    try {
      const supabase = createClient()
      const { data: { session } } = await supabase.auth.getSession()
      
      if (session?.access_token) {
        api.setToken(session.access_token)
      }

      await api.updateProfile({
        full_name: fullName,
        linkedin_url: linkedinUrl,
        resume_text: resumeText,
        skills,
        experience_years: experienceYears ? parseInt(experienceYears) : undefined,
        preferences: {
          target_roles: targetRoles,
          target_locations: targetLocations,
          remote_preference: remotePreference,
          salary_min: salaryMin ? parseInt(salaryMin) * 1000 : undefined,
          salary_max: salaryMax ? parseInt(salaryMax) * 1000 : undefined,
        }
      })

      router.push("/dashboard")
    } catch (err) {
      // If API fails, still redirect (profile will use defaults)
      console.log("[v0] Profile setup error:", err)
      router.push("/dashboard")
    } finally {
      setLoading(false)
    }
  }

  const totalSteps = 4

  return (
    <div className="min-h-screen bg-background flex items-center justify-center p-4">
      <Card className="w-full max-w-2xl border-border">
        <CardHeader className="text-center">
          <Link href="/" className="flex items-center justify-center gap-2 mb-4">
            <Crosshair className="w-8 h-8 text-accent" />
            <span className="text-2xl font-bold">JobSniper AI</span>
          </Link>
          <CardTitle className="text-2xl">Set Up Your Profile</CardTitle>
          <CardDescription>
            Step {step} of {totalSteps} - {
              step === 1 ? "Basic Information" :
              step === 2 ? "Your Resume" :
              step === 3 ? "Skills & Experience" :
              "Job Preferences"
            }
          </CardDescription>
          
          {/* Progress bar */}
          <div className="flex gap-2 mt-4">
            {Array.from({ length: totalSteps }).map((_, i) => (
              <div
                key={i}
                className={`h-2 flex-1 rounded-full transition-colors ${
                  i < step ? "bg-accent" : "bg-muted"
                }`}
              />
            ))}
          </div>
        </CardHeader>

        <CardContent className="space-y-6">
          {error && (
            <div className="p-3 rounded-lg bg-destructive/10 text-destructive text-sm">
              {error}
            </div>
          )}

          {/* Step 1: Basic Info */}
          {step === 1 && (
            <div className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="fullName">Full Name</Label>
                <Input
                  id="fullName"
                  placeholder="John Doe"
                  value={fullName}
                  onChange={(e) => setFullName(e.target.value)}
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="linkedin">LinkedIn Profile URL</Label>
                <Input
                  id="linkedin"
                  placeholder="https://linkedin.com/in/johndoe"
                  value={linkedinUrl}
                  onChange={(e) => setLinkedinUrl(e.target.value)}
                />
                <p className="text-xs text-muted-foreground">
                  We&apos;ll use this to extract your experience and skills
                </p>
              </div>
            </div>
          )}

          {/* Step 2: Resume */}
          {step === 2 && (
            <div className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="resume">Paste Your Resume</Label>
                <Textarea
                  id="resume"
                  placeholder="Paste your resume text here... Our AI will analyze it to craft personalized applications."
                  value={resumeText}
                  onChange={(e) => setResumeText(e.target.value)}
                  className="min-h-[300px]"
                />
                <p className="text-xs text-muted-foreground">
                  The Ghostwriter agent will use this to tailor your applications
                </p>
              </div>
            </div>
          )}

          {/* Step 3: Skills */}
          {step === 3 && (
            <div className="space-y-4">
              <div className="space-y-2">
                <Label>Your Skills</Label>
                <div className="flex gap-2">
                  <Input
                    placeholder="Add a skill (e.g., Python, React, Project Management)"
                    value={newSkill}
                    onChange={(e) => setNewSkill(e.target.value)}
                    onKeyDown={(e) => e.key === "Enter" && (e.preventDefault(), addSkill())}
                  />
                  <Button type="button" onClick={addSkill} size="icon">
                    <Plus className="h-4 w-4" />
                  </Button>
                </div>
                <div className="flex flex-wrap gap-2 mt-2">
                  {skills.map((skill) => (
                    <Badge key={skill} variant="secondary" className="gap-1">
                      {skill}
                      <button onClick={() => removeSkill(skill)}>
                        <X className="h-3 w-3" />
                      </button>
                    </Badge>
                  ))}
                </div>
              </div>
              <div className="space-y-2">
                <Label htmlFor="experience">Years of Experience</Label>
                <Input
                  id="experience"
                  type="number"
                  placeholder="5"
                  value={experienceYears}
                  onChange={(e) => setExperienceYears(e.target.value)}
                />
              </div>
            </div>
          )}

          {/* Step 4: Preferences */}
          {step === 4 && (
            <div className="space-y-4">
              <div className="space-y-2">
                <Label>Target Roles</Label>
                <div className="flex gap-2">
                  <Input
                    placeholder="Add a role (e.g., Software Engineer, Product Manager)"
                    value={newRole}
                    onChange={(e) => setNewRole(e.target.value)}
                    onKeyDown={(e) => e.key === "Enter" && (e.preventDefault(), addRole())}
                  />
                  <Button type="button" onClick={addRole} size="icon">
                    <Plus className="h-4 w-4" />
                  </Button>
                </div>
                <div className="flex flex-wrap gap-2 mt-2">
                  {targetRoles.map((role) => (
                    <Badge key={role} variant="secondary" className="gap-1">
                      {role}
                      <button onClick={() => removeRole(role)}>
                        <X className="h-3 w-3" />
                      </button>
                    </Badge>
                  ))}
                </div>
              </div>

              <div className="space-y-2">
                <Label>Target Locations</Label>
                <div className="flex gap-2">
                  <Input
                    placeholder="Add a location (e.g., San Francisco, Remote)"
                    value={newLocation}
                    onChange={(e) => setNewLocation(e.target.value)}
                    onKeyDown={(e) => e.key === "Enter" && (e.preventDefault(), addLocation())}
                  />
                  <Button type="button" onClick={addLocation} size="icon">
                    <Plus className="h-4 w-4" />
                  </Button>
                </div>
                <div className="flex flex-wrap gap-2 mt-2">
                  {targetLocations.map((location) => (
                    <Badge key={location} variant="secondary" className="gap-1">
                      {location}
                      <button onClick={() => removeLocation(location)}>
                        <X className="h-3 w-3" />
                      </button>
                    </Badge>
                  ))}
                </div>
              </div>

              <div className="space-y-2">
                <Label>Remote Preference</Label>
                <div className="flex gap-2">
                  {["remote", "hybrid", "onsite", "any"].map((pref) => (
                    <Button
                      key={pref}
                      type="button"
                      variant={remotePreference === pref ? "default" : "outline"}
                      size="sm"
                      onClick={() => setRemotePreference(pref)}
                      className="capitalize"
                    >
                      {pref}
                    </Button>
                  ))}
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="salaryMin">Min Salary ($k)</Label>
                  <Input
                    id="salaryMin"
                    type="number"
                    placeholder="100"
                    value={salaryMin}
                    onChange={(e) => setSalaryMin(e.target.value)}
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="salaryMax">Max Salary ($k)</Label>
                  <Input
                    id="salaryMax"
                    type="number"
                    placeholder="200"
                    value={salaryMax}
                    onChange={(e) => setSalaryMax(e.target.value)}
                  />
                </div>
              </div>
            </div>
          )}

          {/* Navigation */}
          <div className="flex justify-between pt-4">
            <Button
              variant="outline"
              onClick={() => setStep(step - 1)}
              disabled={step === 1}
            >
              <ArrowLeft className="mr-2 h-4 w-4" />
              Back
            </Button>

            {step < totalSteps ? (
              <Button onClick={() => setStep(step + 1)}>
                Next
                <ArrowRight className="ml-2 h-4 w-4" />
              </Button>
            ) : (
              <Button onClick={handleSubmit} disabled={loading}>
                {loading ? (
                  <Loader2 className="h-4 w-4 animate-spin" />
                ) : (
                  <>
                    Complete Setup
                    <ArrowRight className="ml-2 h-4 w-4" />
                  </>
                )}
              </Button>
            )}
          </div>

          {/* Skip link */}
          <div className="text-center">
            <Button
              variant="link"
              className="text-muted-foreground"
              onClick={() => router.push("/dashboard")}
            >
              Skip for now
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
