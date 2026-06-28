"use client";

import { useEffect, useRef, useState } from "react";
import MessageBubble from "./MessageBubble";
import { getMessages, sendMessage } from "@/lib/api";
import { Message } from "@/lib/types";

interface Props {
  conversationId: string | null;
  onNewConversation: (id: string) => void;
}

export default function ChatWindow({ conversationId, onNewConversation }: Props) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [sending, setSending] = useState(false);
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!conversationId) { setMessages([]); return; }
    getMessages(conversationId).then(setMessages).catch(() => {});
  }, [conversationId]);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  async function submit() {
    const text = input.trim();
    if (!text || sending) return;
    setInput("");
    setSending(true);

    const userMsg: Message = { role: "user", content: text, created_at: new Date().toISOString() };
    setMessages((prev) => [...prev, userMsg]);

    try {
      const res = await sendMessage(text, conversationId ?? undefined);
      if (!conversationId) onNewConversation(res.conversation_id);
      const assistantMsg: Message = {
        role: "assistant",
        content: res.reply,
        created_at: new Date().toISOString(),
      };
      setMessages((prev) => [...prev, assistantMsg]);
    } catch {
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: "Something went wrong. Please try again.", created_at: new Date().toISOString() },
      ]);
    } finally {
      setSending(false);
    }
  }

  function handleKeyDown(e: React.KeyboardEvent<HTMLTextAreaElement>) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      submit();
    }
  }

  return (
    <>
      <div className="chat-area">
        {messages.length === 0 && !sending && (
          <div className="empty-state">
            <h2>What can I help with?</h2>
            <p>Ask me to search your email, check your calendar, or just chat.</p>
          </div>
        )}
        {messages.map((m, i) => (
          <MessageBubble key={i} message={m} />
        ))}
        {sending && (
          <div className="bubble assistant" style={{ opacity: 0.5 }}>
            thinking...
          </div>
        )}
        <div ref={bottomRef} />
      </div>

      <div className="input-area">
        <div className="input-row">
          <textarea
            className="chat-input"
            rows={1}
            placeholder="Message deskpilot..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
          />
          <button className="send-btn" onClick={submit} disabled={!input.trim() || sending}>
            ↑
          </button>
        </div>
      </div>
    </>
  );
}
