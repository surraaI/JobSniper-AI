import { Crosshair } from "lucide-react"
import Link from "next/link"

export function Footer() {
  return (
    <footer className="border-t border-border py-12 px-4">
      <div className="max-w-6xl mx-auto">
        <div className="flex flex-col md:flex-row items-center justify-between gap-6">
          <Link href="/" className="flex items-center gap-2 font-bold text-lg">
            <Crosshair className="w-5 h-5 text-accent" />
            <span>JobSniper</span>
            <span className="text-accent">AI</span>
          </Link>

          <nav className="flex items-center gap-6 text-sm text-muted-foreground">
            <Link href="/privacy" className="hover:text-foreground transition-colors">Privacy</Link>
            <Link href="/terms" className="hover:text-foreground transition-colors">Terms</Link>
            <Link href="/contact" className="hover:text-foreground transition-colors">Contact</Link>
          </nav>

          <p className="text-sm text-muted-foreground">
            &copy; {new Date().getFullYear()} JobSniper AI. All rights reserved.
          </p>
        </div>
      </div>
    </footer>
  )
}
