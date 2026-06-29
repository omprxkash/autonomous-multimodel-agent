"use client";

import { useState, useRef, useEffect, useCallback } from "react";
import { Send, Loader2 } from "lucide-react";
import { STREAM_URL, API_URL } from "@/config/api";
import { EmailCard } from "@/components/ui/email-card";
import { EventCard } from "@/components/ui/event-card";
import { DraftCard } from "@/components/ui/draft-card";
import { ActionCard } from "@/components/ui/action-card";

interface Message {
  role: "user" | "assistant";
  content: string;
}

// ---------------------------------------------------------------------------
// Message formatter — parses special markers from the agent response
// ---------------------------------------------------------------------------

function parseEmailDraft(text: string) {
  const match = text.match(
    /\*\*\*EMAIL_DRAFT\*\*\*([\s\S]*?)\*\*\*END_EMAIL_DRAFT\*\*\*/
  );
  if (!match) return null;
  const block = match[1];
  const to = (block.match(/^To:\s*(.+)$/m) ?? [])[1]?.trim() ?? "";
  const subject = (block.match(/^Subject:\s*(.+)$/m) ?? [])[1]?.trim() ?? "";
  const body = block.replace(/^To:.*$/m, "").replace(/^Subject:.*$/m, "").trim();
  return { to, subject, body };
}

function parseEmails(text: string): { from: string; subject: string; snippet: string }[] {
  const emails: { from: string; subject: string; snippet: string }[] = [];
  const re = /(\d+)\.\s*📧\s*(.*?)\n\s*Subject:\s*(.*?)\n\s*Preview:\s*(.*?)(?=\n\d+\.|$)/gs;
  let m;
  while ((m = re.exec(text)) !== null) {
    emails.push({ from: m[2].trim(), subject: m[3].trim(), snippet: m[4].trim() });
  }
  return emails;
}

function parseEvents(text: string): { title: string; start: string; end?: string }[] {
  const events: { title: string; start: string; end?: string }[] = [];
  const re = /(\d+)\.\s*📅\s*(.*?)\n\s*(?:When|Time):\s*(.*?)(?:\s*[-–]\s*(.*?))?(?=\n\d+\.|$)/gs;
  let m;
  while ((m = re.exec(text)) !== null) {
    events.push({ title: m[2].trim(), start: m[3].trim(), end: m[4]?.trim() });
  }
  return events;
}

// ---------------------------------------------------------------------------
// Message renderer
// ---------------------------------------------------------------------------

function AssistantMessage({ content }: { content: string }) {
  const draft = parseEmailDraft(content);
  const emails = parseEmails(content);
  const events = parseEvents(content);

  const cleanedText = content
    .replace(/\*\*\*EMAIL_DRAFT\*\*\*[\s\S]*?\*\*\*END_EMAIL_DRAFT\*\*\*/, "")
    .trim();

  return (
    <div className="space-y-3">
      {cleanedText && (
        <div className="text-sm text-white/80 leading-relaxed whitespace-pre-wrap">
          {cleanedText}
        </div>
      )}

      {draft && (
        <DraftCard to={draft.to} subject={draft.subject} body={draft.body} />
      )}

      {emails.length > 0 && (
        <div className="space-y-2">
          {emails.map((e, i) => (
            <EmailCard key={i} from={e.from} subject={e.subject} snippet={e.snippet} index={i + 1} />
          ))}
        </div>
      )}

      {events.length > 0 && (
        <div className="space-y-2">
          {events.map((ev, i) => (
            <EventCard key={i} title={ev.title} start={ev.start} end={ev.end} />
          ))}
        </div>
      )}
    </div>
  );
}

// ---------------------------------------------------------------------------
// Main Chat component
// ---------------------------------------------------------------------------

export default function Chat() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [streaming, setStreaming] = useState(false);
  const [conversationId, setConversationId] = useState<string | null>(null);
  const bottomRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const sendMessage = useCallback(async () => {
    const text = input.trim();
    if (!text || streaming) return;

    setInput("");
    setMessages((prev) => [...prev, { role: "user", content: text }]);
    setStreaming(true);

    const token = localStorage.getItem("dp_token");
    let assistantContent = "";
    setMessages((prev) => [...prev, { role: "assistant", content: "" }]);

    try {
      const res = await fetch(STREAM_URL, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ message: text, conversation_id: conversationId }),
      });

      if (!res.ok || !res.body) throw new Error("Stream failed");

      const reader = res.body.getReader();
      const decoder = new TextDecoder();

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        const lines = decoder.decode(value, { stream: true }).split("\n");
        for (const line of lines) {
          if (!line.startsWith("data: ")) continue;
          try {
            const evt = JSON.parse(line.slice(6));
            if (evt.type === "start" && evt.conversation_id) {
              setConversationId(evt.conversation_id);
            } else if (evt.type === "chunk") {
              assistantContent += evt.content;
              setMessages((prev) => {
                const copy = [...prev];
                copy[copy.length - 1] = { role: "assistant", content: assistantContent };
                return copy;
              });
            }
          } catch {
            /* skip malformed */
          }
        }
      }
    } catch (err) {
      // Fallback to regular chat endpoint
      try {
        const res = await fetch(`${API_URL}/chat/message`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify({ message: text, conversation_id: conversationId }),
        });
        const data = await res.json();
        if (data.conversation_id) setConversationId(data.conversation_id);
        assistantContent = data.reply ?? "Something went wrong.";
        setMessages((prev) => {
          const copy = [...prev];
          copy[copy.length - 1] = { role: "assistant", content: assistantContent };
          return copy;
        });
      } catch {
        setMessages((prev) => {
          const copy = [...prev];
          copy[copy.length - 1] = { role: "assistant", content: "Connection error. Please try again." };
          return copy;
        });
      }
    } finally {
      setStreaming(false);
      inputRef.current?.focus();
    }
  }, [input, streaming, conversationId]);

  function handleKeyDown(e: React.KeyboardEvent<HTMLTextAreaElement>) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  }

  return (
    <div className="flex flex-col h-full">
      {/* Messages */}
      <div className="flex-1 overflow-y-auto px-4 py-4 space-y-4">
        {messages.length === 0 && (
          <div className="flex flex-col items-center justify-center h-full text-center space-y-3 opacity-50">
            <div className="text-3xl">✦</div>
            <p className="text-sm text-white/60">Ask me to check your inbox, schedule meetings, or draft replies.</p>
          </div>
        )}

        {messages.map((msg, i) => (
          <div
            key={i}
            className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}
          >
            {msg.role === "user" ? (
              <div className="max-w-[75%] rounded-2xl px-4 py-2.5 bg-purple-600 text-white text-sm">
                {msg.content}
              </div>
            ) : (
              <div className="max-w-[85%] rounded-2xl px-4 py-3 bg-white/5 border border-white/10 backdrop-blur-md">
                {msg.content === "" && streaming ? (
                  <div className="flex gap-1 items-center py-1">
                    {[0, 1, 2].map((i) => (
                      <span
                        key={i}
                        className="w-1.5 h-1.5 rounded-full bg-purple-400 animate-bounce"
                        style={{ animationDelay: `${i * 0.15}s` }}
                      />
                    ))}
                  </div>
                ) : (
                  <AssistantMessage content={msg.content} />
                )}
              </div>
            )}
          </div>
        ))}
        <div ref={bottomRef} />
      </div>

      {/* Input */}
      <div className="px-4 py-3 border-t border-white/10">
        <div className="flex items-end gap-2 rounded-2xl border border-white/10 bg-white/5 px-3 py-2">
          <textarea
            ref={inputRef}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Message deskpilot…"
            rows={1}
            className="flex-1 bg-transparent text-sm text-white/90 placeholder-white/30 resize-none focus:outline-none max-h-32"
            style={{ height: "auto" }}
            onInput={(e) => {
              const el = e.currentTarget;
              el.style.height = "auto";
              el.style.height = `${el.scrollHeight}px`;
            }}
          />
          <button
            onClick={sendMessage}
            disabled={!input.trim() || streaming}
            className="shrink-0 w-8 h-8 rounded-xl bg-purple-600 hover:bg-purple-500 disabled:opacity-30 disabled:cursor-not-allowed flex items-center justify-center transition-all"
          >
            {streaming ? (
              <Loader2 className="w-3.5 h-3.5 animate-spin text-white" />
            ) : (
              <Send className="w-3.5 h-3.5 text-white" />
            )}
          </button>
        </div>
      </div>
    </div>
  );
}
