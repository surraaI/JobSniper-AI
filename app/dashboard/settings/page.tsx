"use client"

import { useState, useEffect } from "react"
import { useRouter } from "next/navigation"
import { createClient } from "@/lib/supabase/client"
import { Header } from "@/components/landing/header"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Switch } from "@/components/ui/switch"
import { Badge } from "@/components/ui/badge"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import {
  MessageCircle,
  Mail,
  Bell,
  ArrowLeft,
  Loader2,
  CheckCircle,
  AlertCircle,
  Unlink,
  Link as LinkIcon,
  Settings,
  Copy,
  ExternalLink,
} from "lucide-react"

interface NotificationPreferences {
  email_job_matches?: boolean
  email_application_responses?: boolean
  email_interviews?: boolean
  email_offers?: boolean
  telegram_enabled?: boolean
  telegram_job_matches?: boolean
  telegram_interviews?: boolean
  telegram_offers?: boolean
  whatsapp_enabled?: boolean
}

export default function SettingsPage() {
  const router = useRouter()
  const [user, setUser] = useState<{ id: string; email: string } | null>(null)
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [connecting, setConnecting] = useState<string | null>(null)
  const [telegramChatId, setTelegramChatId] = useState("")
  const [gmailConnected, setGmailConnected] = useState(false)
  const [whatsappConnected, setWhatsappConnected] = useState(false)
  const [preferences, setPreferences] = useState<NotificationPreferences>({
    email_job_matches: true,
    email_application_responses: true,
    email_interviews: true,
    email_offers: true,
    telegram_enabled: false,
    telegram_job_matches: true,
    telegram_interviews: true,
    telegram_offers: true,
    whatsapp_enabled: false,
  })
  const [success, setSuccess] = useState<string | null>(null)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const checkAuth = async () => {
      const supabase = createClient()
      const { data: { user } } = await supabase.auth.getUser()

      if (!user) {
        router.push("/auth/login")
        return
      }

      setUser({ id: user.id, email: user.email || "" })

      // Load preferences from Supabase
      const { data: profileData } = await supabase
        .from("profiles")
        .select("*")
        .eq("id", user.id)
        .single()

      if (profileData) {
        setTelegramChatId(profileData.telegram_chat_id || "")
        if (profileData.notification_preferences) {
          setPreferences(profileData.notification_preferences)
        }
        setGmailConnected(!!profileData.gmail_connected)
        setWhatsappConnected(!!profileData.whatsapp_connected)
      }

      setLoading(false)
    }

    checkAuth()
  }, [router])

  const handleConnectTelegram = async () => {
    setConnecting("telegram")
    setError(null)
    setSuccess(null)

    // Show Telegram bot instructions
    const telegramBotLink = `https://t.me/JobSniperAIBot?start=${user?.id}`

    // Copy to clipboard
    try {
      await navigator.clipboard.writeText(telegramBotLink)
      setSuccess("Telegram bot link copied! Click the button below to connect.")
    } catch (err) {
      setSuccess("Open the Telegram bot link manually to connect")
    }

    setConnecting(null)
  }

  const handleDisconnectTelegram = async () => {
    if (!user) return
    setSaving(true)
    setError(null)

    try {
      const supabase = createClient()
      await supabase
        .from("profiles")
        .update({ telegram_chat_id: null })
        .eq("id", user.id)

      setTelegramChatId("")
      setPreferences({ ...preferences, telegram_enabled: false })
      setSuccess("Telegram disconnected successfully")
    } catch (err) {
      setError("Failed to disconnect Telegram")
    } finally {
      setSaving(false)
    }
  }

  const handleConnectGmail = async () => {
    setConnecting("gmail")
    setError(null)

    // In a real app, this would open an OAuth flow
    // For now, show instructions
    setSuccess("Gmail integration would open OAuth flow to connect your Gmail account")
    setConnecting(null)
  }

  const handleConnectWhatsapp = async () => {
    setConnecting("whatsapp")
    setError(null)

    // Show WhatsApp connection instructions
    setSuccess("WhatsApp integration would use Twilio to verify your phone number")
    setConnecting(null)
  }

  const handleSavePreferences = async () => {
    if (!user) return
    setSaving(true)
    setError(null)

    try {
      const supabase = createClient()
      await supabase
        .from("profiles")
        .update({
          notification_preferences: preferences,
        })
        .eq("id", user.id)

      setSuccess("Notification preferences saved!")
    } catch (err) {
      setError("Failed to save preferences")
    } finally {
      setSaving(false)
    }
  }

  const updatePreference = (key: keyof NotificationPreferences, value: boolean) => {
    setPreferences({ ...preferences, [key]: value })
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-background">
        <Header />
        <div className="flex items-center justify-center h-screen">
          <Loader2 className="w-8 h-8 animate-spin text-accent" />
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-background">
      <Header />
      <div className="pt-20 pb-12">
        <div className="max-w-4xl mx-auto px-4">
          {/* Header */}
          <div className="flex items-center gap-4 mb-8">
            <Button variant="ghost" size="icon" onClick={() => router.push("/dashboard")}>
              <ArrowLeft className="w-5 h-5" />
            </Button>
            <div>
              <h1 className="text-3xl font-bold flex items-center gap-2">
                <Settings className="w-8 h-8 text-accent" />
                Notification Settings
              </h1>
              <p className="text-muted-foreground mt-1">Manage your notification integrations and preferences</p>
            </div>
          </div>

          {/* Status Messages */}
          {success && (
            <div className="mb-6 p-4 bg-green-500/10 border border-green-500/20 rounded-lg flex items-center gap-2 text-green-700 dark:text-green-400">
              <CheckCircle className="w-5 h-5" />
              <p>{success}</p>
            </div>
          )}

          {error && (
            <div className="mb-6 p-4 bg-red-500/10 border border-red-500/20 rounded-lg flex items-center gap-2 text-red-700 dark:text-red-400">
              <AlertCircle className="w-5 h-5" />
              <p>{error}</p>
            </div>
          )}

          <Tabs defaultValue="integrations" className="w-full">
            <TabsList className="grid w-full grid-cols-2">
              <TabsTrigger value="integrations">Integrations</TabsTrigger>
              <TabsTrigger value="preferences">Preferences</TabsTrigger>
            </TabsList>

            {/* Integrations Tab */}
            <TabsContent value="integrations" className="space-y-6 mt-6">
              {/* Telegram */}
              <Card>
                <CardHeader>
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-3">
                      <div className="w-10 h-10 rounded-lg bg-[#0088cc]/10 flex items-center justify-center">
                        <MessageCircle className="w-5 h-5 text-[#0088cc]" />
                      </div>
                      <div>
                        <CardTitle>Telegram Bot</CardTitle>
                        <CardDescription>Get job matches and updates directly on Telegram</CardDescription>
                      </div>
                    </div>
                    {telegramChatId && (
                      <Badge variant="secondary" className="bg-green-500/10 text-green-700 dark:text-green-400">
                        <CheckCircle className="w-3 h-3 mr-1" />
                        Connected
                      </Badge>
                    )}
                  </div>
                </CardHeader>
                <CardContent className="space-y-4">
                  {telegramChatId ? (
                    <>
                      <div className="p-3 bg-muted rounded-lg">
                        <p className="text-sm text-muted-foreground mb-2">Chat ID:</p>
                        <div className="flex items-center gap-2">
                          <code className="text-sm font-mono flex-1 break-all">{telegramChatId}</code>
                          <Button
                            variant="ghost"
                            size="icon"
                            onClick={() => navigator.clipboard.writeText(telegramChatId)}
                          >
                            <Copy className="w-4 h-4" />
                          </Button>
                        </div>
                      </div>
                      <Button
                        variant="destructive"
                        className="w-full"
                        onClick={handleDisconnectTelegram}
                        disabled={saving}
                      >
                        <Unlink className="w-4 h-4 mr-2" />
                        Disconnect Telegram
                      </Button>
                    </>
                  ) : (
                    <>
                      <div className="space-y-2 text-sm">
                        <p className="text-muted-foreground">
                          Connect your Telegram account to receive job matches, interview invitations, and offer notifications.
                        </p>
                        <ol className="list-decimal list-inside space-y-1 text-muted-foreground">
                          <li>Click the button below to open Telegram Bot</li>
                          <li>Start the conversation with the bot</li>
                          <li>Your Telegram will be linked automatically</li>
                        </ol>
                      </div>
                      <div className="flex gap-2">
                        <Button
                          className="flex-1"
                          onClick={handleConnectTelegram}
                          disabled={connecting === "telegram"}
                        >
                          {connecting === "telegram" ? (
                            <Loader2 className="w-4 h-4 animate-spin mr-2" />
                          ) : (
                            <LinkIcon className="w-4 h-4 mr-2" />
                          )}
                          Connect Telegram
                        </Button>
                        <Button
                          variant="outline"
                          asChild
                        >
                          <a href="https://t.me/JobSniperAIBot" target="_blank" rel="noopener noreferrer">
                            <ExternalLink className="w-4 h-4" />
                          </a>
                        </Button>
                      </div>
                    </>
                  )}
                </CardContent>
              </Card>

              {/* Gmail */}
              <Card>
                <CardHeader>
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-3">
                      <div className="w-10 h-10 rounded-lg bg-red-500/10 flex items-center justify-center">
                        <Mail className="w-5 h-5 text-red-500" />
                      </div>
                      <div>
                        <CardTitle>Gmail Monitoring</CardTitle>
                        <CardDescription>Monitor responses to your job applications</CardDescription>
                      </div>
                    </div>
                    {gmailConnected && (
                      <Badge variant="secondary" className="bg-green-500/10 text-green-700 dark:text-green-400">
                        <CheckCircle className="w-3 h-3 mr-1" />
                        Connected
                      </Badge>
                    )}
                  </div>
                </CardHeader>
                <CardContent className="space-y-4">
                  <p className="text-sm text-muted-foreground">
                    Grant JobSniper AI access to monitor your Gmail inbox for job application responses. We only track emails from recruiters and hiring teams.
                  </p>
                  <Button
                    className="w-full"
                    onClick={handleConnectGmail}
                    disabled={connecting === "gmail" || gmailConnected}
                  >
                    {connecting === "gmail" ? (
                      <Loader2 className="w-4 h-4 animate-spin mr-2" />
                    ) : gmailConnected ? (
                      <CheckCircle className="w-4 h-4 mr-2" />
                    ) : (
                      <LinkIcon className="w-4 h-4 mr-2" />
                    )}
                    {gmailConnected ? "Gmail Connected" : "Connect Gmail"}
                  </Button>
                </CardContent>
              </Card>

              {/* WhatsApp */}
              <Card>
                <CardHeader>
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-3">
                      <div className="w-10 h-10 rounded-lg bg-[#25d366]/10 flex items-center justify-center">
                        <MessageCircle className="w-5 h-5 text-[#25d366]" />
                      </div>
                      <div>
                        <CardTitle>WhatsApp Notifications</CardTitle>
                        <CardDescription>Receive alerts via WhatsApp messages</CardDescription>
                      </div>
                    </div>
                    {whatsappConnected && (
                      <Badge variant="secondary" className="bg-green-500/10 text-green-700 dark:text-green-400">
                        <CheckCircle className="w-3 h-3 mr-1" />
                        Connected
                      </Badge>
                    )}
                  </div>
                </CardHeader>
                <CardContent className="space-y-4">
                  <p className="text-sm text-muted-foreground">
                    Verify your phone number to receive WhatsApp notifications for urgent job alerts and interview invitations.
                  </p>
                  <Button
                    className="w-full"
                    onClick={handleConnectWhatsapp}
                    disabled={connecting === "whatsapp" || whatsappConnected}
                  >
                    {connecting === "whatsapp" ? (
                      <Loader2 className="w-4 h-4 animate-spin mr-2" />
                    ) : whatsappConnected ? (
                      <CheckCircle className="w-4 h-4 mr-2" />
                    ) : (
                      <LinkIcon className="w-4 h-4 mr-2" />
                    )}
                    {whatsappConnected ? "WhatsApp Connected" : "Connect WhatsApp"}
                  </Button>
                </CardContent>
              </Card>
            </TabsContent>

            {/* Preferences Tab */}
            <TabsContent value="preferences" className="space-y-6 mt-6">
              {/* Email Preferences */}
              <Card>
                <CardHeader>
                  <div className="flex items-center gap-2">
                    <Mail className="w-5 h-5 text-red-500" />
                    <CardTitle>Email Notifications</CardTitle>
                  </div>
                  <CardDescription>Control which email notifications you receive</CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="flex items-center justify-between p-3 rounded-lg bg-muted/50">
                    <div>
                      <p className="font-medium text-sm">Job Matches Found</p>
                      <p className="text-xs text-muted-foreground">Get notified when new jobs match your criteria</p>
                    </div>
                    <Switch
                      checked={preferences.email_job_matches ?? true}
                      onCheckedChange={(val) => updatePreference("email_job_matches", val)}
                    />
                  </div>

                  <div className="flex items-center justify-between p-3 rounded-lg bg-muted/50">
                    <div>
                      <p className="font-medium text-sm">Application Responses</p>
                      <p className="text-xs text-muted-foreground">Get notified of rejections and next steps</p>
                    </div>
                    <Switch
                      checked={preferences.email_application_responses ?? true}
                      onCheckedChange={(val) => updatePreference("email_application_responses", val)}
                    />
                  </div>

                  <div className="flex items-center justify-between p-3 rounded-lg bg-muted/50">
                    <div>
                      <p className="font-medium text-sm">Interview Invitations</p>
                      <p className="text-xs text-muted-foreground">Get notified of interview schedule invites</p>
                    </div>
                    <Switch
                      checked={preferences.email_interviews ?? true}
                      onCheckedChange={(val) => updatePreference("email_interviews", val)}
                    />
                  </div>

                  <div className="flex items-center justify-between p-3 rounded-lg bg-muted/50">
                    <div>
                      <p className="font-medium text-sm">Job Offers</p>
                      <p className="text-xs text-muted-foreground">Get notified when you receive an offer</p>
                    </div>
                    <Switch
                      checked={preferences.email_offers ?? true}
                      onCheckedChange={(val) => updatePreference("email_offers", val)}
                    />
                  </div>
                </CardContent>
              </Card>

              {/* Telegram Preferences */}
              {telegramChatId && (
                <Card>
                  <CardHeader>
                    <div className="flex items-center gap-2">
                      <MessageCircle className="w-5 h-5 text-[#0088cc]" />
                      <CardTitle>Telegram Notifications</CardTitle>
                    </div>
                    <CardDescription>Control what you receive on Telegram</CardDescription>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div className="flex items-center justify-between p-3 rounded-lg bg-muted/50">
                      <div>
                        <p className="font-medium text-sm">Job Matches</p>
                        <p className="text-xs text-muted-foreground">Get Telegram alerts for new matches</p>
                      </div>
                      <Switch
                        checked={preferences.telegram_job_matches ?? true}
                        onCheckedChange={(val) => updatePreference("telegram_job_matches", val)}
                      />
                    </div>

                    <div className="flex items-center justify-between p-3 rounded-lg bg-muted/50">
                      <div>
                        <p className="font-medium text-sm">Interview Invitations</p>
                        <p className="text-xs text-muted-foreground">Get urgent Telegram alerts</p>
                      </div>
                      <Switch
                        checked={preferences.telegram_interviews ?? true}
                        onCheckedChange={(val) => updatePreference("telegram_interviews", val)}
                      />
                    </div>

                    <div className="flex items-center justify-between p-3 rounded-lg bg-muted/50">
                      <div>
                        <p className="font-medium text-sm">Job Offers</p>
                        <p className="text-xs text-muted-foreground">Get Telegram notification on offers</p>
                      </div>
                      <Switch
                        checked={preferences.telegram_offers ?? true}
                        onCheckedChange={(val) => updatePreference("telegram_offers", val)}
                      />
                    </div>
                  </CardContent>
                </Card>
              )}

              {/* Save Button */}
              <Button onClick={handleSavePreferences} disabled={saving} className="w-full" size="lg">
                {saving ? (
                  <Loader2 className="w-4 h-4 animate-spin mr-2" />
                ) : (
                  <Bell className="w-4 h-4 mr-2" />
                )}
                Save Preferences
              </Button>
            </TabsContent>
          </Tabs>
        </div>
      </div>
    </div>
  )
}
