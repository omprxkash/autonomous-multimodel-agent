"use client";

import { Mail, Calendar, CheckCircle2, XCircle } from "lucide-react";
import { API_URL } from "@/config/api";

interface User {
  gmail_connected?: boolean;
  calendar_connected?: boolean;
}

interface Props {
  user: User | null;
}

export function IntegrationPanel({ user }: Props) {
  const integrations = [
    {
      id: "gmail",
      label: "Gmail",
      icon: Mail,
      connected: user?.gmail_connected ?? false,
    },
    {
      id: "calendar",
      label: "Calendar",
      icon: Calendar,
      connected: user?.calendar_connected ?? false,
    },
  ];

  function connect() {
    const token = localStorage.getItem("dp_token");
    window.location.href = `${API_URL}/auth/login?token=${token}`;
  }

  return (
    <div className="rounded-xl border border-white/10 bg-white/5 backdrop-blur-md overflow-hidden">
      <div className="px-4 py-3 border-b border-white/10">
        <span className="text-sm font-semibold text-white">Integrations</span>
      </div>

      <div className="p-3 space-y-2">
        {integrations.map(({ id, label, icon: Icon, connected }) => (
          <div
            key={id}
            className="flex items-center justify-between rounded-lg bg-white/5 border border-white/10 px-3 py-2.5"
          >
            <div className="flex items-center gap-2">
              <Icon className="w-4 h-4 text-purple-400" />
              <span className="text-sm text-white/80">{label}</span>
            </div>

            {connected ? (
              <div className="flex items-center gap-1 text-green-400 text-xs">
                <CheckCircle2 className="w-3.5 h-3.5" />
                <span>Connected</span>
              </div>
            ) : (
              <button
                onClick={connect}
                className="flex items-center gap-1 text-xs text-white/40 hover:text-white transition-colors"
              >
                <XCircle className="w-3.5 h-3.5" />
                <span>Connect</span>
              </button>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
