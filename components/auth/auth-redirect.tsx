"use client"

import { useEffect } from "react"
import { useRouter, useSearchParams } from "next/navigation"
import { createClient } from "@/lib/supabase/client"

export function AuthRedirect() {
  const router = useRouter()
  const searchParams = useSearchParams()
  
  useEffect(() => {
    const code = searchParams.get("code")
    
    const handleAuth = async () => {
      const supabase = createClient()
      
      // Check if there's an auth code (user just signed up/in)
      if (code) {
        const { error } = await supabase.auth.exchangeCodeForSession(code)
        
        if (!error) {
          // Check if user has completed profile setup
          const { data: { user } } = await supabase.auth.getUser()
          
          if (user) {
            const { data: profile } = await supabase
              .from("profiles")
              .select("id")
              .eq("id", user.id)
              .single()
            
            // If profile exists, go to dashboard; otherwise go to setup
            if (profile) {
              router.push("/dashboard")
            } else {
              router.push("/profile/setup")
            }
          }
        } else {
          router.push("/auth/error")
        }
      } else {
        // No auth code - check if user is already logged in
        const { data: { user } } = await supabase.auth.getUser()
        
        if (user) {
          // User is logged in, redirect to dashboard
          router.push("/dashboard")
        }
        // If not logged in and no code, stay on home page
      }
    }
    
    handleAuth()
  }, [searchParams, router])
  
  return null
}
