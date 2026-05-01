"use client"

import { useEffect } from "react"
import { useRouter, useSearchParams } from "next/navigation"
import { createClient } from "@/lib/supabase/client"

export function AuthRedirect() {
  const router = useRouter()
  const searchParams = useSearchParams()
  
  useEffect(() => {
    const code = searchParams.get("code")
    
    if (code) {
      const handleAuth = async () => {
        const supabase = createClient()
        const { error } = await supabase.auth.exchangeCodeForSession(code)
        
        if (!error) {
          router.push("/profile/setup")
        } else {
          router.push("/auth/error")
        }
      }
      
      handleAuth()
    }
  }, [searchParams, router])
  
  return null
}
