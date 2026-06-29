"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import ChatWindow from "@/components/ChatWindow";
import MemoryPanel from "@/components/MemoryPanel";
import { getMe, listConversations } from "@/lib/api";
import { clearToken, isAuthenticated, loginWithGoogle } from "@/lib/auth";
import { Conversation, User } from "@/lib/types";

export default function Home() {
  const router = useRouter();
  const [user, setUser] = useState<User | null>(null);
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [activeConvId, setActiveConvId] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!isAuthenticated()) { setLoading(false); return; }
    Promise.all([getMe(), listConversations()])
      .then(([u, convs]) => { setUser(u); setConversations(convs); })
      .catch(() => clearToken())
      .finally(() => setLoading(false));
  }, []);

  function handleNewConversation(id: string) {
    setActiveConvId(id);
    listConversations().then(setConversations).catch(() => {});
  }

  if (loading) {
    return (
      <div style={{ display: "flex", alignItems: "center", justifyContent: "center", height: "100vh", color: "var(--muted)" }}>
        Loading...
      </div>
    );
  }

  if (!user) {
    return (
      <div style={{ display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", height: "100vh", gap: 20 }}>
        <div style={{ fontSize: 28, fontWeight: 700, letterSpacing: -0.5 }}>
          desk<span style={{ color: "var(--accent-light)" }}>pilot</span>
        </div>
        <div style={{ color: "var(--muted)", marginBottom: 8 }}>Your agentic workspace assistant</div>
        <button className="btn btn-primary" onClick={loginWithGoogle}>
          Sign in with Google
        </button>
      </div>
    );
  }

  return (
    <div className="layout">
      <aside className="sidebar">
        <div className="logo">desk<span>pilot</span></div>

        <button
          className="btn btn-outline"
          style={{ width: "100%", marginBottom: 8 }}
          onClick={() => setActiveConvId(null)}
        >
          + New chat
        </button>

        {conversations.map((c) => (
          <div
            key={c.id}
            className={`conv-item${c.id === activeConvId ? " active" : ""}`}
            onClick={() => setActiveConvId(c.id)}
          >
            {c.title || "Untitled"}
          </div>
        ))}

        <div style={{ flex: 1 }} />

        <div style={{ borderTop: "1px solid var(--glass-border)", paddingTop: 12, marginTop: 8 }}>
          <MemoryPanel />
          <div
            style={{
              display: "flex",
              alignItems: "center",
              gap: 10,
              padding: "10px 12px",
              borderRadius: 10,
              cursor: "pointer",
            }}
            className="glass-hover"
            onClick={() => router.push("/profile")}
          >
            {user.picture && (
              <img src={user.picture} alt="" style={{ width: 28, height: 28, borderRadius: "50%" }} />
            )}
            <div style={{ overflow: "hidden" }}>
              <div style={{ fontSize: 13, fontWeight: 500, whiteSpace: "nowrap", overflow: "hidden", textOverflow: "ellipsis" }}>
                {user.name}
              </div>
              <div style={{ fontSize: 11, color: "var(--muted)" }}>{user.email}</div>
            </div>
          </div>
        </div>
      </aside>

      <main className="main">
        <ChatWindow conversationId={activeConvId} onNewConversation={handleNewConversation} />
      </main>
    </div>
  );
}
