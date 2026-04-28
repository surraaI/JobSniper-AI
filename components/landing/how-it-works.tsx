import { Upload, Crosshair, CheckCircle, MessageCircle, Mail, Bell } from "lucide-react"

const steps = [
  {
    icon: Upload,
    step: "01",
    title: "Upload Your Profile",
    description: "Share your resume, LinkedIn URL, and job preferences. Tell us what you&apos;re looking for - roles, salary, location, culture.",
  },
  {
    icon: Crosshair,
    step: "02",
    title: "Sniper Mode Activates",
    description: "Your agents scan global job boards for high-probability matches. Thousands of opportunities analyzed, best ones surfaced.",
  },
  {
    icon: MessageCircle,
    step: "03",
    title: "One-Tap Approval",
    description: "Get curated opportunities on Telegram/WhatsApp. Approve applications with a tap - full control, zero grind.",
  },
  {
    icon: CheckCircle,
    step: "04",
    title: "Applications Deployed",
    description: "Approved jobs receive personalized applications automatically. Track everything in your War Room dashboard.",
  },
  {
    icon: Mail,
    step: "05",
    title: "Sentinel Monitors Inbox",
    description: "Your email is monitored for recruiter replies, interview invites, and technical assessments. Statuses update automatically.",
  },
  {
    icon: Bell,
    step: "06",
    title: "Never Miss a Reply",
    description: "High-priority alerts for interview requests and deadlines. The agent even suggests next steps when you get a rejection.",
  },
]

export function HowItWorks() {
  return (
    <section className="py-24 px-4 bg-secondary/30">
      <div className="max-w-6xl mx-auto">
        <div className="text-center mb-16">
          <p className="text-accent font-mono text-sm tracking-widest uppercase mb-4">
            How It Works
          </p>
          <h2 className="text-4xl md:text-5xl font-bold tracking-tight mb-4 text-balance">
            The full loop. Automated.
          </h2>
          <p className="text-muted-foreground text-lg max-w-2xl mx-auto text-pretty">
            Set it up once. Let the agents do the heavy lifting while you focus on what matters.
          </p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
          {steps.map((step) => (
            <div key={step.step} className="relative">
              <div className="flex flex-col items-start">
                <span className="text-6xl font-bold text-accent/20 mb-4">{step.step}</span>
                <div className="p-3 rounded-lg bg-accent/10 text-accent mb-4">
                  <step.icon className="w-6 h-6" />
                </div>
                <h3 className="text-xl font-semibold mb-2">{step.title}</h3>
                <p className="text-muted-foreground text-sm">{step.description}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
