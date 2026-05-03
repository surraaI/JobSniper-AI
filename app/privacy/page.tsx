import { Header } from "@/components/landing/header"
import { Footer } from "@/components/landing/footer"

export const metadata = {
  title: "Privacy Policy - JobSniper AI",
  description: "Privacy policy for JobSniper AI",
}

export default function PrivacyPage() {
  return (
    <div className="min-h-screen bg-background text-foreground">
      <Header hideAuthButtons={true} />
      <main className="pt-32 pb-16">
        <div className="max-w-4xl mx-auto px-4">
          <h1 className="text-4xl font-bold mb-8">Privacy Policy</h1>
          
          <div className="prose prose-invert max-w-none space-y-6">
            <section>
              <h2 className="text-2xl font-bold mb-4">Introduction</h2>
              <p className="text-muted-foreground">
                JobSniper AI (&quot;we&quot; or &quot;us&quot;) is committed to protecting your privacy. This Privacy Policy explains our data practices and your privacy rights.
              </p>
            </section>

            <section>
              <h2 className="text-2xl font-bold mb-4">Information We Collect</h2>
              <p className="text-muted-foreground mb-4">
                We collect information you provide directly, such as:
              </p>
              <ul className="list-disc list-inside space-y-2 text-muted-foreground">
                <li>Account information (email, name, LinkedIn profile)</li>
                <li>Resume and work experience data</li>
                <li>Job preferences and search criteria</li>
                <li>Communication preferences</li>
                <li>Notification contact information (Telegram, Gmail, WhatsApp)</li>
              </ul>
            </section>

            <section>
              <h2 className="text-2xl font-bold mb-4">How We Use Your Information</h2>
              <p className="text-muted-foreground mb-4">
                We use your information to:
              </p>
              <ul className="list-disc list-inside space-y-2 text-muted-foreground">
                <li>Provide and improve our job matching services</li>
                <li>Send job alerts and application updates</li>
                <li>Personalize your experience</li>
                <li>Communicate with you about your account</li>
                <li>Monitor and analyze usage patterns</li>
              </ul>
            </section>

            <section>
              <h2 className="text-2xl font-bold mb-4">Data Security</h2>
              <p className="text-muted-foreground">
                We implement industry-standard security measures to protect your personal information. However, no method of transmission over the internet is 100% secure. We cannot guarantee absolute security of your data.
              </p>
            </section>

            <section>
              <h2 className="text-2xl font-bold mb-4">Third-Party Services</h2>
              <p className="text-muted-foreground mb-4">
                Our service integrates with:
              </p>
              <ul className="list-disc list-inside space-y-2 text-muted-foreground">
                <li>Supabase for authentication and data storage</li>
                <li>Telegram Bot API for notifications</li>
                <li>Gmail API for email monitoring</li>
                <li>Job listing APIs (Adzuna and others)</li>
              </ul>
            </section>

            <section>
              <h2 className="text-2xl font-bold mb-4">Your Rights</h2>
              <p className="text-muted-foreground mb-4">
                You have the right to:
              </p>
              <ul className="list-disc list-inside space-y-2 text-muted-foreground">
                <li>Access your personal data</li>
                <li>Request deletion of your account and data</li>
                <li>Opt-out of communications</li>
                <li>Update your information</li>
              </ul>
            </section>

            <section>
              <h2 className="text-2xl font-bold mb-4">Contact Us</h2>
              <p className="text-muted-foreground">
                For privacy inquiries, please contact us at: <a href="mailto:privacy@jobsniper.ai" className="text-accent hover:underline">privacy@jobsniper.ai</a>
              </p>
            </section>

            <section>
              <h2 className="text-2xl font-bold mb-4">Changes to This Policy</h2>
              <p className="text-muted-foreground">
                We may update this policy from time to time. We will notify you of significant changes by posting the new policy on this page.
              </p>
            </section>

            <p className="text-sm text-muted-foreground pt-8 border-t border-border">
              Last updated: {new Date().toLocaleDateString()}
            </p>
          </div>
        </div>
      </main>
      <Footer />
    </div>
  )
}
