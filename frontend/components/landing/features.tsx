import { Shield, Clock, Target, BarChart3, Lock, Zap, Mail, CalendarCheck, FileText } from "lucide-react"

const features = [
  {
    icon: Shield,
    title: "Human in the Loop",
    description: "Every application requires your approval. Full control, zero surprise submissions.",
  },
  {
    icon: Mail,
    title: "Email Monitoring",
    description: "Sentinel watches your inbox for recruiter replies, interview invites, and status updates.",
  },
  {
    icon: CalendarCheck,
    title: "Interview Detection",
    description: "Automatically detects Calendly links and scheduling requests. High-priority alerts sent instantly.",
  },
  {
    icon: FileText,
    title: "Assessment Tracking",
    description: "Extracts deadlines and requirements from technical assessments and screening questionnaires.",
  },
  {
    icon: Target,
    title: "Precision Matching",
    description: "AI that understands nuance - not just keywords, but culture fit and growth potential.",
  },
  {
    icon: BarChart3,
    title: "Auto Status Updates",
    description: "Application statuses update automatically based on email replies from companies.",
  },
  {
    icon: Clock,
    title: "24/7 Operation",
    description: "Sniper hunts while Sentinel guards. Your job search runs around the clock.",
  },
  {
    icon: Zap,
    title: "Smart Notifications",
    description: "Telegram/WhatsApp alerts for opportunities AND recruiter responses. Never miss a beat.",
  },
  {
    icon: Lock,
    title: "Privacy First",
    description: "Your data stays encrypted. Email access is read-only and scoped to job-related messages.",
  },
]

export function Features() {
  return (
    <section className="py-24 px-4">
      <div className="max-w-6xl mx-auto">
        <div className="text-center mb-16">
          <p className="text-accent font-mono text-sm tracking-widest uppercase mb-4">
            Features
          </p>
          <h2 className="text-4xl md:text-5xl font-bold tracking-tight mb-4 text-balance">
            Outbound hunting. Inbound monitoring.
          </h2>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
          {features.map((feature) => (
            <div key={feature.title} className="p-6 rounded-xl border border-border bg-card/50 hover:border-accent/30 transition-colors">
              <div className="p-3 rounded-lg bg-accent/10 text-accent w-fit mb-4">
                <feature.icon className="w-5 h-5" />
              </div>
              <h3 className="text-lg font-semibold mb-2">{feature.title}</h3>
              <p className="text-muted-foreground text-sm">{feature.description}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
