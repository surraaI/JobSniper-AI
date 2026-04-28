import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Radar, Brain, PenTool, MessageSquare, Shield, Crosshair } from "lucide-react"
import { Badge } from "@/components/ui/badge"

const sniperAgents = [
  {
    icon: Radar,
    name: "The Scout",
    role: "Opportunity Hunter",
    description: "Constantly scans job boards, company career pages, and hidden opportunities across LinkedIn, Indeed, and niche platforms. Never misses a match.",
  },
  {
    icon: Brain,
    name: "The Strategist",
    role: "Match Analyzer",
    description: "Deeply understands your skills, experience, and goals. Scores and ranks opportunities, identifying the perfect fits you might overlook.",
  },
  {
    icon: PenTool,
    name: "The Ghostwriter",
    role: "Application Crafter",
    description: "Tailors your resume and cover letter for each role. Speaks the company&apos;s language while authentically representing your unique value.",
  },
  {
    icon: MessageSquare,
    name: "The Liaison",
    role: "Outreach Specialist",
    description: "Drafts personalized outreach to recruiters and hiring managers. Builds connections and follows up at the perfect moments.",
  },
]

const sentinelAgent = {
  icon: Shield,
  name: "The Sentinel",
  role: "Inbox Guardian",
  description: "Monitors your email for interview invites, screening requests, and status updates. Instantly alerts you via Telegram/WhatsApp when action is needed - so you never miss a crucial reply.",
  features: [
    "Detects interview invites & Calendly links",
    "Extracts deadlines from technical assessments",
    "Auto-updates application statuses",
    "High-priority alerts for time-sensitive emails",
  ],
}

export function Agents() {
  return (
    <section className="py-24 px-4">
      <div className="max-w-6xl mx-auto">
        <div className="text-center mb-16">
          <p className="text-accent font-mono text-sm tracking-widest uppercase mb-4">
            Meet Your Squad
          </p>
          <h2 className="text-4xl md:text-5xl font-bold tracking-tight mb-4 text-balance">
            Two modes. Full-loop coverage.
          </h2>
          <p className="text-muted-foreground text-lg max-w-2xl mx-auto text-pretty">
            From finding opportunities to managing recruiter responses - your AI Career Chief of Staff handles it all.
          </p>
        </div>

        {/* Sniper Mode */}
        <div className="mb-12">
          <div className="flex items-center gap-3 mb-6">
            <div className="p-2 rounded-lg bg-accent/10 text-accent">
              <Crosshair className="w-5 h-5" />
            </div>
            <h3 className="text-2xl font-bold">Sniper Mode</h3>
            <Badge variant="secondary" className="text-xs">Outbound</Badge>
          </div>
          <p className="text-muted-foreground mb-6 max-w-2xl">
            Autonomous job hunting that finds, matches, and applies to roles while you sleep.
          </p>
          <div className="grid md:grid-cols-2 gap-6">
            {sniperAgents.map((agent) => (
              <Card key={agent.name} className="bg-card border-border hover:border-accent/50 transition-colors">
                <CardHeader>
                  <div className="flex items-center gap-4">
                    <div className="p-3 rounded-lg bg-accent/10 text-accent">
                      <agent.icon className="w-6 h-6" />
                    </div>
                    <div>
                      <CardTitle className="text-xl">{agent.name}</CardTitle>
                      <CardDescription className="text-accent">{agent.role}</CardDescription>
                    </div>
                  </div>
                </CardHeader>
                <CardContent>
                  <p className="text-muted-foreground">{agent.description}</p>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>

        {/* Sentinel Mode */}
        <div>
          <div className="flex items-center gap-3 mb-6">
            <div className="p-2 rounded-lg bg-green-500/10 text-green-500">
              <Shield className="w-5 h-5" />
            </div>
            <h3 className="text-2xl font-bold">Sentinel Mode</h3>
            <Badge className="text-xs bg-green-500/10 text-green-500 hover:bg-green-500/20">Inbound</Badge>
          </div>
          <p className="text-muted-foreground mb-6 max-w-2xl">
            Intelligent email monitoring that ensures no opportunity slips through the cracks.
          </p>
          <Card className="bg-card border-green-500/30 hover:border-green-500/50 transition-colors">
            <CardHeader>
              <div className="flex items-center gap-4">
                <div className="p-3 rounded-lg bg-green-500/10 text-green-500">
                  <sentinelAgent.icon className="w-6 h-6" />
                </div>
                <div>
                  <CardTitle className="text-xl">{sentinelAgent.name}</CardTitle>
                  <CardDescription className="text-green-500">{sentinelAgent.role}</CardDescription>
                </div>
              </div>
            </CardHeader>
            <CardContent>
              <p className="text-muted-foreground mb-4">{sentinelAgent.description}</p>
              <div className="grid sm:grid-cols-2 gap-2">
                {sentinelAgent.features.map((feature) => (
                  <div key={feature} className="flex items-center gap-2 text-sm text-muted-foreground">
                    <div className="w-1.5 h-1.5 rounded-full bg-green-500" />
                    {feature}
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </section>
  )
}
