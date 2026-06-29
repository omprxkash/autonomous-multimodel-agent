"use client";

import { useState } from "react";
import { X, Loader2, Send } from "lucide-react";
import { API_URL } from "@/config/api";

interface Suggestion {
  type: string;
  subject: string;
  body: string;
}

interface Props {
  open: boolean;
  onOpenChange: (v: boolean) => void;
  emailFrom: string;
  emailSubject: string;
  emailBody: string;
  emailId?: string;
}

export function EmailReplyDialog({
  open,
  onOpenChange,
  emailFrom,
  emailSubject,
  emailBody,
  emailId,
}: Props) {
  const [loading, setLoading] = useState(false);
  const [suggestions, setSuggestions] = useState<Suggestion[]>([]);
  const [selected, setSelected] = useState<Suggestion | null>(null);
  const [body, setBody] = useState("");
  const [sending, setSending] = useState(false);
  const [sent, setSent] = useState(false);

  if (!open) return null;

  async function loadSuggestions() {
    setLoading(true);
    try {
      const token = localStorage.getItem("dp_token");
      const res = await fetch(`${API_URL}/email/suggest-replies`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          email_from: emailFrom,
          email_subject: emailSubject,
          email_body: emailBody,
          email_id: emailId,
        }),
      });
      const data = await res.json();
      setSuggestions(data.suggestions ?? []);
    } catch {
      /* ignore */
    } finally {
      setLoading(false);
    }
  }

  function pickSuggestion(s: Suggestion) {
    setSelected(s);
    setBody(s.body);
  }

  async function sendReply() {
    setSending(true);
    try {
      const token = localStorage.getItem("dp_token");
      await fetch(`${API_URL}/email/send`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          to: emailFrom,
          subject: selected?.subject ?? `Re: ${emailSubject}`,
          body,
          reply_to_message_id: emailId,
        }),
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
          <h3 className="text-sm font-semibold text-white">Reply to {emailFrom}</h3>
          <button onClick={() => onOpenChange(false)} className="text-white/40 hover:text-white transition-colors">
            <X className="w-4 h-4" />
          </button>
        </div>

        <div className="p-5 space-y-4">
          {sent ? (
            <p className="text-green-400 text-sm text-center py-4">Reply sent successfully.</p>
          ) : (
            <>
              {suggestions.length === 0 && !loading && (
                <button
                  onClick={loadSuggestions}
                  className="w-full py-2 rounded-lg bg-purple-600 hover:bg-purple-500 text-white text-sm transition-all"
                >
                  Generate reply suggestions
                </button>
              )}

              {loading && (
                <div className="flex items-center justify-center py-6">
                  <Loader2 className="w-5 h-5 animate-spin text-purple-400" />
                </div>
              )}

              {suggestions.length > 0 && (
                <div className="grid grid-cols-3 gap-2">
                  {suggestions.map((s) => (
                    <button
                      key={s.type}
                      onClick={() => pickSuggestion(s)}
                      className={`text-xs py-1.5 rounded-lg border transition-all capitalize ${
                        selected?.type === s.type
                          ? "border-purple-400 bg-purple-500/20 text-purple-300"
                          : "border-white/10 text-white/50 hover:border-white/30"
                      }`}
                    >
                      {s.type}
                    </button>
                  ))}
                </div>
              )}

              {selected && (
                <textarea
                  value={body}
                  onChange={(e) => setBody(e.target.value)}
                  rows={6}
                  className="w-full text-sm bg-white/5 border border-white/10 rounded-lg px-3 py-2 text-white/90 resize-none focus:outline-none focus:border-purple-400/60"
                />
              )}

              {selected && (
                <button
                  onClick={sendReply}
                  disabled={sending}
                  className="w-full flex items-center justify-center gap-2 py-2 rounded-lg bg-purple-600 hover:bg-purple-500 disabled:opacity-50 text-white text-sm transition-all"
                >
                  {sending ? <Loader2 className="w-4 h-4 animate-spin" /> : <Send className="w-4 h-4" />}
                  {sending ? "Sending…" : "Send Reply"}
                </button>
              )}
            </>
          )}
        </div>
      </div>
    </div>
  );
}
