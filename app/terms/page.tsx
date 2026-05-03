import { Header } from "@/components/landing/header"
import { Footer } from "@/components/landing/footer"

export const metadata = {
  title: "Terms of Service - JobSniper AI",
  description: "Terms of Service for JobSniper AI",
}

export default function TermsPage() {
  return (
    <div className="min-h-screen bg-background text-foreground">
      <Header hideAuthButtons={true} />
      <main className="pt-32 pb-16">
        <div className="max-w-4xl mx-auto px-4">
          <h1 className="text-4xl font-bold mb-8">Terms of Service</h1>
          
          <div className="prose prose-invert max-w-none space-y-6">
            <section>
              <h2 className="text-2xl font-bold mb-4">1. Acceptance of Terms</h2>
              <p className="text-muted-foreground">
                By accessing and using JobSniper AI, you accept and agree to be bound by the terms and provision of this agreement. If you do not agree to abide by the above, please do not use this service.
              </p>
            </section>

            <section>
              <h2 className="text-2xl font-bold mb-4">2. Use License</h2>
              <p className="text-muted-foreground mb-4">
                Permission is granted to temporarily download one copy of the materials (information or software) on JobSniper AI for personal, non-commercial transitory viewing only. This is the grant of a license, not a transfer of title, and under this license you may not:
              </p>
              <ul className="list-disc list-inside space-y-2 text-muted-foreground">
                <li>Modify or copy the materials</li>
                <li>Use the materials for any commercial purpose or for any public display</li>
                <li>Attempt to decompile or reverse engineer any software contained on the site</li>
                <li>Remove any copyright or other proprietary notations from the materials</li>
                <li>Transfer the materials to another person or &quot;mirror&quot; the materials on any other server</li>
              </ul>
            </section>

            <section>
              <h2 className="text-2xl font-bold mb-4">3. Disclaimer</h2>
              <p className="text-muted-foreground">
                The materials on JobSniper AI are provided on an &quot;as is&quot; basis. JobSniper AI makes no warranties, expressed or implied, and hereby disclaims and negates all other warranties including, without limitation, implied warranties or conditions of merchantability, fitness for a particular purpose, or non-infringement of intellectual property or other violation of rights.
              </p>
            </section>

            <section>
              <h2 className="text-2xl font-bold mb-4">4. Limitations</h2>
              <p className="text-muted-foreground">
                In no event shall JobSniper AI or its suppliers be liable for any damages (including, without limitation, damages for loss of data or profit, or due to business interruption) arising out of the use or inability to use the materials on JobSniper AI, even if JobSniper AI or an authorized representative has been notified orally or in writing of the possibility of such damage.
              </p>
            </section>

            <section>
              <h2 className="text-2xl font-bold mb-4">5. Accuracy of Materials</h2>
              <p className="text-muted-foreground">
                The materials appearing on JobSniper AI could include technical, typographical, or photographic errors. JobSniper AI does not warrant that any of the materials on its website are accurate, complete, or current. JobSniper AI may make changes to the materials contained on its website at any time without notice.
              </p>
            </section>

            <section>
              <h2 className="text-2xl font-bold mb-4">6. Links</h2>
              <p className="text-muted-foreground">
                JobSniper AI has not reviewed all of the sites linked to its website and is not responsible for the contents of any such linked site. The inclusion of any link does not imply endorsement by JobSniper AI of the site. Use of any such linked website is at the user&apos;s own risk.
              </p>
            </section>

            <section>
              <h2 className="text-2xl font-bold mb-4">7. Modifications</h2>
              <p className="text-muted-foreground">
                JobSniper AI may revise these terms of service for its website at any time without notice. By using this website, you are agreeing to be bound by the then current version of these terms of service.
              </p>
            </section>

            <section>
              <h2 className="text-2xl font-bold mb-4">8. Governing Law</h2>
              <p className="text-muted-foreground">
                These terms and conditions are governed by and construed in accordance with the laws of United States, and you irrevocably submit to the exclusive jurisdiction of the courts in that location.
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
