"use client";

import { useState } from "react";
import { X, Send, Loader2 } from "lucide-react";
import { API_URL } from "@/config/api";

interface Props {
  open: boolean;
  onOpenChange: (v: boolean) => void;
  initialTo?: string;
  initialSubject?: string;
  initialBody?: string;
}

export function ComposeEmailDialog({
  open,
  onOpenChange,
  initialTo = "",
  initialSubject = "",
  initialBody = "",
}: Props) {
  const [to, setTo] = useState(initialTo);
  const [subject, setSubject] = useState(initialSubject);
  const [body, setBody] = useState(initialBody);
  const [sending, setSending] = useState(false);
  const [sent, setSent] = useState(false);

  if (!open) return null;

  async function handleSend() {
    setSending(true);
    try {
      const token = localStorage.getItem("dp_token");
      await fetch(`${API_URL}/email/send`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ to, subject, body }),
      });
      setSent(true);
    } catch {
      /* ignore */
    } finally {
      setSending(false);
    }
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4">
      <div className="w-full max-w-lg bg-[#18181b] rounded-2xl border border-white/10 shadow-2xl overflow-hidden">
        <div className="flex items-center justify-between px-5 py-4 border-b border-white/10">
          <h3 className="text-sm font-semibold text-white">New Email</h3>
          <button onClick={() => onOpenChange(false)} className="text-white/40 hover:text-white transition-colors">
            <X className="w-4 h-4" />
          </button>
        </div>

        <div className="p-5 space-y-3">
          {sent ? (
            <p className="text-green-400 text-sm text-center py-4">Email sent successfully.</p>
          ) : (
            <>
              {[
                { label: "To", value: to, onChange: setTo },
                { label: "Subject", value: subject, onChange: setSubject },
              ].map(({ label, value, onChange }) => (
                <div key={label} className="flex gap-3 items-center border-b border-white/10 pb-2">
                  <span className="text-xs text-white/40 w-14 shrink-0">{label}</span>
                  <input
                    value={value}
                    onChange={(e) => onChange(e.target.value)}
                    className="flex-1 bg-transparent text-sm text-white/90 focus:outline-none"
                  />
                </div>
              ))}

              <textarea
                value={body}
                onChange={(e) => setBody(e.target.value)}
                rows={7}
                placeholder="Write your message…"
                className="w-full text-sm bg-white/5 border border-white/10 rounded-lg px-3 py-2 text-white/90 resize-none focus:outline-none focus:border-purple-400/60 placeholder-white/20"
              />

              <button
                onClick={handleSend}
                disabled={sending || !to || !subject}
                className="w-full flex items-center justify-center gap-2 py-2 rounded-lg bg-purple-600 hover:bg-purple-500 disabled:opacity-40 text-white text-sm transition-all"
              >
                {sending ? <Loader2 className="w-4 h-4 animate-spin" /> : <Send className="w-4 h-4" />}
                {sending ? "Sending…" : "Send"}
              </button>
            </>
          )}
        </div>
      </div>
    </div>
  );
}
