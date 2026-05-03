import { Header } from "@/components/landing/header"
import { Footer } from "@/components/landing/footer"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Mail, Crosshair } from "lucide-react"

export const metadata = {
  title: "Contact Us - JobSniper AI",
  description: "Get in touch with JobSniper AI",
}

export default function ContactPage() {
  return (
    <div className="min-h-screen bg-background text-foreground">
      <Header hideAuthButtons={true} />
      <main className="pt-32 pb-16">
        <div className="max-w-4xl mx-auto px-4">
          <div className="text-center mb-12">
            <h1 className="text-4xl font-bold mb-4">Get in Touch</h1>
            <p className="text-lg text-muted-foreground">
              Have questions? We&apos;d love to hear from you. Send us a message and we&apos;ll respond as soon as possible.
            </p>
          </div>

          <div className="grid md:grid-cols-2 gap-8 mb-12">
            <Card className="border-border">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Mail className="w-5 h-5 text-accent" />
                  Email
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-2">
                <p className="text-muted-foreground">For general inquiries:</p>
                <a href="mailto:hello@jobsniper.ai" className="text-accent hover:underline">
                  hello@jobsniper.ai
                </a>
                <p className="text-muted-foreground pt-4">For support:</p>
                <a href="mailto:support@jobsniper.ai" className="text-accent hover:underline">
                  support@jobsniper.ai
                </a>
                <p className="text-muted-foreground pt-4">For partnerships:</p>
                <a href="mailto:partnerships@jobsniper.ai" className="text-accent hover:underline">
                  partnerships@jobsniper.ai
                </a>
              </CardContent>
            </Card>

            <Card className="border-border">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Crosshair className="w-5 h-5 text-accent" />
                  Quick Links
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                <div>
                  <p className="text-sm text-muted-foreground mb-1">Status Page</p>
                  <a href="#" className="text-accent hover:underline">
                    system.jobsniper.ai
                  </a>
                </div>
                <div>
                  <p className="text-sm text-muted-foreground mb-1">Documentation</p>
                  <a href="#" className="text-accent hover:underline">
                    docs.jobsniper.ai
                  </a>
                </div>
                <div>
                  <p className="text-sm text-muted-foreground mb-1">Bug Reports</p>
                  <a href="mailto:bugs@jobsniper.ai" className="text-accent hover:underline">
                    bugs@jobsniper.ai
                  </a>
                </div>
              </CardContent>
            </Card>
          </div>

          <Card className="border-border max-w-2xl mx-auto">
            <CardHeader>
              <CardTitle>Send us a Message</CardTitle>
              <CardDescription>Fill out the form below and we&apos;ll get back to you shortly</CardDescription>
            </CardHeader>
            <CardContent>
              <form className="space-y-4">
                <div className="grid md:grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <label htmlFor="name" className="text-sm font-medium">
                      Name
                    </label>
                    <Input
                      id="name"
                      placeholder="Your name"
                      className="bg-card border-border"
                    />
                  </div>
                  <div className="space-y-2">
                    <label htmlFor="email" className="text-sm font-medium">
                      Email
                    </label>
                    <Input
                      id="email"
                      type="email"
                      placeholder="your@email.com"
                      className="bg-card border-border"
                    />
                  </div>
                </div>
                <div className="space-y-2">
                  <label htmlFor="subject" className="text-sm font-medium">
                    Subject
                  </label>
                  <Input
                    id="subject"
                    placeholder="How can we help?"
                    className="bg-card border-border"
                  />
                </div>
                <div className="space-y-2">
                  <label htmlFor="message" className="text-sm font-medium">
                    Message
                  </label>
                  <Textarea
                    id="message"
                    placeholder="Tell us more..."
                    className="min-h-[150px] bg-card border-border"
                  />
                </div>
                <Button className="w-full">
                  Send Message
                </Button>
                <p className="text-xs text-muted-foreground text-center">
                  We typically respond within 24 hours
                </p>
              </form>
            </CardContent>
          </Card>
        </div>
      </main>
      <Footer />
    </div>
  )
}
