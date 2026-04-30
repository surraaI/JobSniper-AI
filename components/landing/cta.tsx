"use client"

import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { useState } from "react"
import { ArrowRight, CheckCircle, Loader2 } from "lucide-react"
import { createClient } from "@/lib/supabase/client"

export function CTA() {
  const [email, setEmail] = useState("")
  const [submitted, setSubmitted] = useState(false)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!email) return
    
    setLoading(true)
    setError(null)
    
    try {
      // For now, just redirect to signup with email pre-filled
      // In production, you could save to a waitlist table
      window.location.href = `/auth/signup?email=${encodeURIComponent(email)}`
    } catch {
      setSubmitted(true)
    }
  }

  return (
    <section className="py-24 px-4">
      <div className="max-w-4xl mx-auto">
        <div className="relative rounded-2xl border border-border bg-card p-8 md:p-16 overflow-hidden">
          {/* Accent glow */}
          <div className="absolute top-0 right-0 w-[300px] h-[300px] bg-accent/20 rounded-full blur-[100px] pointer-events-none" />
          
          <div className="relative z-10 text-center">
            <h2 className="text-3xl md:text-5xl font-bold tracking-tight mb-4 text-balance">
              Ready to snipe your dream job?
            </h2>
            <p className="text-muted-foreground text-lg max-w-xl mx-auto mb-8 text-pretty">
              Join the waitlist and be first to deploy your AI job hunting squad.
            </p>

            {submitted ? (
              <div className="flex items-center justify-center gap-3 text-accent">
                <CheckCircle className="w-6 h-6" />
                <span className="text-lg font-medium">{"You're on the list! We'll be in touch soon."}</span>
              </div>
            ) : (
              <form onSubmit={handleSubmit} className="flex flex-col sm:flex-row gap-3 max-w-md mx-auto">
                <Input
                  type="email"
                  placeholder="Enter your email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                  className="flex-1 bg-secondary border-border"
                />
                <Button type="submit" size="lg" className="whitespace-nowrap" disabled={loading}>
                  {loading ? (
                    <Loader2 className="w-4 h-4 animate-spin" />
                  ) : (
                    <>
                      Join waitlist
                      <ArrowRight className="ml-2 w-4 h-4" />
                    </>
                  )}
                </Button>
              </form>
            )}
          </div>
        </div>
      </div>
    </section>
  )
}
