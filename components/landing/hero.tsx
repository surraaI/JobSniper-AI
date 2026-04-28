"use client"

import { Button } from "@/components/ui/button"
import { ArrowRight, Crosshair } from "lucide-react"

export function Hero() {
  return (
    <section className="relative min-h-[90vh] flex flex-col items-center justify-center px-4 overflow-hidden">
      {/* Accent glow */}
      <div className="absolute top-1/4 right-1/4 w-[500px] h-[500px] bg-accent/30 rounded-full blur-[150px] pointer-events-none" />
      
      {/* Floating icons background */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none opacity-10">
        <div className="absolute top-20 left-[10%] text-muted-foreground">
          <Crosshair className="w-8 h-8" />
        </div>
        <div className="absolute top-40 right-[15%] text-muted-foreground">
          <Crosshair className="w-6 h-6" />
        </div>
        <div className="absolute bottom-32 left-[20%] text-muted-foreground">
          <Crosshair className="w-10 h-10" />
        </div>
        <div className="absolute bottom-48 right-[25%] text-muted-foreground">
          <Crosshair className="w-5 h-5" />
        </div>
      </div>

      <div className="relative z-10 max-w-4xl mx-auto text-center">
        <p className="text-accent font-mono text-sm tracking-widest uppercase mb-6">
          Your AI Career Chief of Staff
        </p>
        
        <h1 className="text-5xl md:text-7xl lg:text-8xl font-bold tracking-tight leading-[1.1] mb-8">
          <span className="text-balance">Never miss an opportunity </span>
          <span className="text-accent">again.</span>
        </h1>
        
        <p className="text-lg md:text-xl text-muted-foreground max-w-2xl mx-auto mb-10 text-pretty">
          JobSniper AI manages your entire job search lifecycle - from hunting and applying 
          to monitoring your inbox for interview invites. Full-loop automation with you in control.
        </p>
        
        <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
          <Button size="lg" className="px-8 py-6 text-base font-medium">
            Get early access
          </Button>
          <Button variant="outline" size="lg" className="px-8 py-6 text-base font-medium group">
            See how it works
            <ArrowRight className="ml-2 w-4 h-4 group-hover:translate-x-1 transition-transform" />
          </Button>
        </div>
      </div>
    </section>
  )
}
