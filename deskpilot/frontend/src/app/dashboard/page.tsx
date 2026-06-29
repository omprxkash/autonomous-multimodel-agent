"use client";

import { Suspense, useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { LogOut, Loader2, Sparkles } from "lucide-react";
import Chat from "@/components/Chat";
import { IntegrationPanel } from "@/components/IntegrationPanel";
import { CalendarWidget } from "@/components/CalendarWidget";
import { API_URL } from "@/config/api";

interface UserData {
  id: string;
  email: string;
  name: string;
  picture?: string;
  gmail_connected?: boolean;
  calendar_connected?: boolean;
}

function DashboardContent() {
  const router = useRouter();
  const [user, setUser] = useState<UserData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    (async () => {
      let token = localStorage.getItem("dp_token");

      // Accept token from URL (OAuth callback redirect)
      if (!token) {
        const params = new URLSearchParams(window.location.search);
        token = params.get("token");
        if (token) localStorage.setItem("dp_token", token);
      }

      if (!token) {
        router.push("/");
        return;
      }

      try {
        // Try /auth/me first, fall back to /users/me
        let res = await fetch(`${API_URL}/auth/me`, {
          headers: { Authorization: `Bearer ${token}` },
        });
        if (res.status === 404) {
          res = await fetch(`${API_URL}/users/me`, {
            headers: { Authorization: `Bearer ${token}` },
          });
        }
        if (!res.ok) throw new Error("Auth failed");
        setUser(await res.json());
      } catch (err: unknown) {
        setError(err instanceof Error ? err.message : "Authentication failed");
      } finally {
        setLoading(false);
      }
    })();
  }, [router]);

  function logout() {
    localStorage.removeItem("dp_token");
    localStorage.removeItem("dp_user_id");
    router.push("/");
  }

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-[#0c0c0e]">
        <Loader2 className="w-8 h-8 animate-spin text-purple-400" />
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center gap-4 bg-[#0c0c0e] text-white">
        <p className="text-red-400 text-sm">{error}</p>
        <button
          onClick={() => router.push("/")}
          className="text-sm px-4 py-2 rounded-lg bg-white/10 hover:bg-white/20 transition-all"
        >
          Back to Login
        </button>
      </div>
    );
  }

  return (
    <div className="h-screen flex flex-col bg-[#0c0c0e] text-white">
      {/* Header */}
      <header className="flex-none h-12 border-b border-white/10 px-6 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Sparkles className="w-4 h-4 text-purple-400" />
          <span className="font-semibold text-sm">deskpilot</span>
        </div>
        <div className="flex items-center gap-3">
          {user?.picture && (
            <img src={user.picture} alt="" className="w-6 h-6 rounded-full" />
          )}
          <span className="hidden md:block text-xs text-white/40">{user?.email}</span>
          <button
            onClick={logout}
            className="w-7 h-7 flex items-center justify-center rounded-lg hover:bg-white/10 transition-all text-white/40 hover:text-white"
          >
            <LogOut className="w-3.5 h-3.5" />
          </button>
        </div>
      </header>

      {/* Main layout */}
      <main className="flex-1 overflow-hidden px-4 py-3">
        <div className="grid grid-cols-1 lg:grid-cols-[260px_minmax(0,1fr)_260px] gap-3 h-full max-w-[1600px] mx-auto">
          {/* Left sidebar */}
          <div className="hidden lg:flex flex-col gap-3 overflow-y-auto">
            <IntegrationPanel user={user} />
          </div>

          {/* Chat area */}
          <div className="h-full min-w-0 rounded-xl border border-white/10 bg-white/5 backdrop-blur-md overflow-hidden">
            <Chat />
          </div>

          {/* Right sidebar */}
          <div className="hidden lg:flex flex-col gap-3 overflow-y-auto">
            <CalendarWidget />
          </div>
        </div>
      </main>
    </div>
  );
}

export default function Dashboard() {
  return (
    <Suspense
      fallback={
        <div className="min-h-screen flex items-center justify-center bg-[#0c0c0e]">
          <Loader2 className="w-8 h-8 animate-spin text-purple-400" />
        </div>
      }
    >
      <DashboardContent />
    </Suspense>
  );
}
