import { Header } from "@/components/landing/header"
import { JobsTracker } from "@/components/jobs/jobs-tracker"

export const metadata = {
  title: "Applied Jobs - JobSniper AI",
  description: "Track all your job applications in one place",
}

export default function JobsPage() {
  return (
    <div className="min-h-screen bg-background text-foreground">
      <Header />
      <main className="pt-24 pb-16">
        <div className="container mx-auto px-4">
          <div className="mb-8">
            <h1 className="text-3xl font-bold mb-2">Applied Jobs</h1>
            <p className="text-muted-foreground">
              Track all applications submitted by your AI squad
            </p>
          </div>
          <JobsTracker />
        </div>
      </main>
    </div>
  )
}
