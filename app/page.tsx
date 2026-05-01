import { Suspense } from "react"
import { Header } from "@/components/landing/header"
import { Hero } from "@/components/landing/hero"
import { Agents } from "@/components/landing/agents"
import { HowItWorks } from "@/components/landing/how-it-works"
import { Features } from "@/components/landing/features"
import { CTA } from "@/components/landing/cta"
import { Footer } from "@/components/landing/footer"
import { AuthRedirect } from "@/components/auth/auth-redirect"

export default function Home() {
  return (
    <main className="min-h-screen">
      <Suspense fallback={null}>
        <AuthRedirect />
      </Suspense>
      <Header />
      <div className="pt-16">
        <Hero />
        <section id="agents">
          <Agents />
        </section>
        <section id="how-it-works">
          <HowItWorks />
        </section>
        <section id="features">
          <Features />
        </section>
        <CTA />
        <Footer />
      </div>
    </main>
  )
}
