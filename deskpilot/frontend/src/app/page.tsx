"use client";

import { useEffect, useRef, useState, Suspense } from "react";
import { useSearchParams, useRouter } from "next/navigation";
import axios from "axios";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

const API = process.env.NEXT_PUBLIC_API_URL || "";

type Msg = { role: "user" | "assistant"; content: string };
type Conv = { id: string; title: string };
type User = {
  id: string; email: string; name: string; picture: string | null;
  is_setup_complete: boolean; job_title: string | null;
  personalization: string; main_goal: string | null; work_hours: string | null;
};

function getToken() { return typeof window !== "undefined" ? localStorage.getItem("dp_token") : null; }
function getUserId() { return typeof window !== "undefined" ? localStorage.getItem("dp_user_id") : null; }
function authHeader() { const t = getToken(); return t ? { Authorization: `Bearer ${t}` } : {}; }

function HomeInner() {
  const searchParams = useSearchParams();

  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [sending, setSending] = useState(false);
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState<Msg[]>([]);
  const [conversations, setConversations] = useState<Conv[]>([]);
  const [currentConvId, setCurrentConvId] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [draftEmail, setDraftEmail] = useState("");
  const [showDraft, setShowDraft] = useState(false);
  const [calendarDraft, setCalendarDraft] = useState<{ title: string; date: string; time: string; description: string } | null>(null);
  const [setupData, setSetupData] = useState({ name: "", job_title: "", main_goal: "", work_hours: "", personalization: "" });
  const [showProfile, setShowProfile] = useState(false);
  const [profileData, setProfileData] = useState({ name: "", job_title: "", main_goal: "", work_hours: "", personalization: "" });
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (error) { const t = setTimeout(() => setError(null), 5000); return () => clearTimeout(t); }
  }, [error]);

  useEffect(() => { bottomRef.current?.scrollIntoView({ behavior: "smooth" }); }, [messages, sending]);

  useEffect(() => {
    const urlError = searchParams.get("error");
    if (urlError) setError(decodeURIComponent(urlError));
    const warn = localStorage.getItem("dp_warning");
    if (warn) { setError(warn); localStorage.removeItem("dp_warning"); }

    const t = getToken();
    const uid = getUserId();
    if (!t || !uid) { setLoading(false); return; }

    (async () => {
      try {
        const { data } = await axios.get(`${API}/api/auth/user/${uid}`);
        setUser(data);
        setProfileData({ name: data.name || "", job_title: data.job_title || "", main_goal: data.main_goal || "", work_hours: data.work_hours || "", personalization: data.personalization || "" });
        if (data.is_setup_complete) await loadConversations(uid);
      } catch {
        localStorage.removeItem("dp_token"); localStorage.removeItem("dp_user_id"); localStorage.removeItem("dp_setup");
      } finally { setLoading(false); }
    })();
  }, []);

  async function loadConversations(uid: string) {
    try {
      const { data } = await axios.get(`${API}/api/chat/conversations`, { headers: authHeader() });
      setConversations(data);
      if (data.length > 0) { setCurrentConvId(data[0].id); await loadHistory(data[0].id); }
    } catch { }
  }

  async function loadHistory(convId: string) {
    try {
      const { data } = await axios.get(`${API}/api/chat/conversations/${convId}/messages`, { headers: authHeader() });
      setMessages(data.map((m: any) => ({ role: m.role, content: m.content })));
    } catch { }
  }

  async function handleLogin() {
    try { const { data } = await axios.get(`${API}/api/auth/login`); window.location.href = data.auth_url; }
    catch { setError("Failed to start login"); }
  }

  function handleLogout() {
    ["dp_token", "dp_user_id", "dp_setup"].forEach(k => localStorage.removeItem(k));
    setUser(null); setMessages([]); setConversations([]);
  }

  async function handleSetup() {
    if (!setupData.name || !setupData.job_title || !setupData.main_goal) { setError("Fill in name, position, and goal."); return; }
    setSending(true);
    try {
      await axios.post(`${API}/api/auth/setup`, { user_id: getUserId(), ...setupData });
      localStorage.setItem("dp_setup", "1");
      setUser(u => u ? { ...u, ...setupData, is_setup_complete: true } : u);
      setMessages([{ role: "assistant", content: `Welcome, ${setupData.name}! How can I help you today?` }]);
      await loadConversations(getUserId()!);
    } catch { setError("Setup failed. Please try again."); }
    finally { setSending(false); }
  }

  async function handleUpdateProfile() {
    setSending(true);
    try {
      await axios.post(`${API}/api/auth/profile/${getUserId()}`, profileData);
      setUser(u => u ? { ...u, ...profileData } : u);
      setShowProfile(false);
    } catch { setError("Profile update failed."); }
    finally { setSending(false); }
  }

  async function sendMsg(overrideMsg?: string) {
    const text = (overrideMsg || message).trim();
    if (!text || sending) return;
    if (!overrideMsg) setMessage("");
    setMessages(prev => [...prev, { role: "user", content: text }]);
    setSending(true);
    try {
      const { data } = await axios.post(`${API}/api/chat/message`, { message: text, conversation_id: currentConvId }, { headers: authHeader() });
      if (!currentConvId) {
        setCurrentConvId(data.conversation_id);
        setConversations(prev => [{ id: data.conversation_id, title: data.title || "New Chat" }, ...prev]);
      }
      const reply: string = data.reply;
      if (reply.includes("--- DRAFT START ---")) {
        const dc = reply.split("--- DRAFT START ---")[1].split("--- DRAFT END ---")[0].trim();
        setDraftEmail(dc); setShowDraft(true); setCalendarDraft(null);
        setMessages(prev => [...prev, { role: "assistant", content: "I prepared a draft below. Edit it or ask me to change anything before sending." }]);
      } else if (reply.includes("--- CALENDAR START ---")) {
        const cal = reply.split("--- CALENDAR START ---")[1].split("--- CALENDAR END ---")[0].trim();
        const lines = cal.split("\n");
        const get = (p: string) => lines.find(l => l.startsWith(p))?.split(":").slice(1).join(":").trim() || "";
        setCalendarDraft({ title: get("Title:"), date: get("Date:"), time: get("Time:"), description: get("Description:") });
        setShowDraft(false);
        setMessages(prev => [...prev, { role: "assistant", content: reply }]);
      } else {
        setShowDraft(false); setCalendarDraft(null);
        setMessages(prev => [...prev, { role: "assistant", content: reply }]);
      }
    } catch (err: any) {
      const msg = err.response?.data?.detail || "Something went wrong. Please try again.";
      setError(typeof msg === "string" ? msg : JSON.stringify(msg));
      setMessages(prev => [...prev, { role: "assistant", content: "I encountered an error. Please try again." }]);
    } finally { setSending(false); }
  }

  async function handleSendDraft() {
    if (!draftEmail.trim()) return;
    setSending(true);
    try {
      const toM = draftEmail.match(/To:\s*([^\n\r]+)/i);
      const subM = draftEmail.match(/Subject:\s*([^\n\r]+)/i);
      const bodyM = draftEmail.match(/Body:\s*([\s\S]+)/i);
      const rawTo = toM?.[1].trim() || "";
      const emailOnly = rawTo.match(/[\w.\-+]+@[\w.\-]+\.\w+/)?.[0] || rawTo;
      const subject = subM?.[1].trim() || "Email from deskpilot";
      const body = bodyM?.[1].trim() || draftEmail;
      await axios.post(`${API}/api/gmail/send`, { user_id: getUserId(), to: emailOnly, subject, body });
      setShowDraft(false); setDraftEmail("");
      setMessages(prev => [...prev, { role: "assistant", content: `Email sent to ${emailOnly}.` }]);
    } catch (err: any) { setError(err.response?.data?.detail || "Failed to send email."); }
    finally { setSending(false); }
  }

  async function handleClearHistory() {
    if (!confirm("Clear all your chat history?")) return;
    try { await axios.delete(`${API}/api/chat/history/${getUserId()}`); setMessages([]); setConversations([]); setCurrentConvId(null); }
    catch { setError("Failed to clear history."); }
  }

  async function handleWipeData() {
    if (!confirm("CRITICAL: Delete ALL your data? This includes chats and everything the agent has learned about you. This cannot be undone.")) return;
    try { await axios.delete(`${API}/api/chat/user/data/${getUserId()}`); setMessages([]); setConversations([]); setCurrentConvId(null); }
    catch { setError("Failed to wipe data."); }
  }

  async function switchConv(id: string) {
    if (id === currentConvId) return;
    setCurrentConvId(id); setShowDraft(false); setDraftEmail(""); setCalendarDraft(null);
    await loadHistory(id);
  }

  if (loading) return <div className="center-screen"><div className="spinner" /></div>;

  if (!user) {
    return (
      <>
        <div className="bg-mesh" />
        <div className="center-screen">
          <div className="glass-card onboarding-card">
            <h1 className="logo-text" style={{ fontSize: "2.5rem", marginBottom: 12 }}>deskpilot</h1>
            <p style={{ color: "var(--text-muted)", marginBottom: 36 }}>Your agentic workspace assistant. Manage email, calendar, and knowledge — with memory.</p>
            <button className="btn-primary" style={{ width: "100%", padding: "14px", fontSize: "1rem" }} onClick={handleLogin}>Continue with Google</button>
            {error && <p style={{ color: "#ef4444", marginTop: 16, fontSize: "0.875rem" }}>{error}</p>}
          </div>
        </div>
      </>
    );
  }

  if (!user.is_setup_complete) {
    return (
      <>
        <div className="bg-mesh" />
        <div className="center-screen">
          <div className="glass-card onboarding-card animate-slide-up">
            <h2 style={{ fontSize: "1.75rem", marginBottom: 8 }}>Welcome!</h2>
            <p style={{ color: "var(--text-muted)", marginBottom: 28 }}>Let me learn a bit about you so I can serve you better.</p>
            <div style={{ display: "flex", flexDirection: "column", gap: 20 }}>
              <div><label className="field-label">Your name</label><input className="input-field" value={setupData.name} onChange={e => setSetupData({ ...setupData, name: e.target.value })} placeholder="e.g. Jordan" /></div>
              <div>
                <label className="field-label">Position</label>
                <select className="input-field" value={setupData.job_title} onChange={e => setSetupData({ ...setupData, job_title: e.target.value })} style={{ background: "var(--glass)", cursor: "pointer" }}>
                  <option value="">Select…</option>
                  <option>Student</option><option>Employee</option><option>Business Owner</option><option>Freelancer</option><option>Researcher</option><option>Other</option>
                </select>
              </div>
              <div>
                <label className="field-label">Main goal</label>
                <textarea className="input-field" style={{ minHeight: 72, resize: "none" }} value={setupData.main_goal} onChange={e => setSetupData({ ...setupData, main_goal: e.target.value })} placeholder="e.g. Tame my inbox and stay ahead of my calendar" />
              </div>
              <button className="btn-primary" style={{ marginTop: 8, height: 52, fontSize: "1rem", width: "100%" }} onClick={handleSetup} disabled={sending}>{sending ? "Setting up…" : "Get started"}</button>
              {error && <p style={{ color: "#ef4444", fontSize: "0.875rem" }}>{error}</p>}
            </div>
          </div>
        </div>
      </>
    );
  }

  return (
    <>
      <div className="bg-mesh" />
      <div className="chat-container">
        <header className="header">
          <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
            <div style={{ width: 38, height: 38, borderRadius: 10, background: "var(--primary)", display: "flex", alignItems: "center", justifyContent: "center", fontWeight: 700 }}>D</div>
            <div>
              <h2 className="logo-text" style={{ fontSize: "1.4rem" }}>deskpilot</h2>
              {user.name && <p style={{ color: "var(--text-muted)", fontSize: "0.75rem" }}>Connected as {user.name}</p>}
            </div>
          </div>
          <div style={{ display: "flex", gap: 8 }}>
            <button className="btn-secondary" onClick={() => { setProfileData({ name: user.name || "", job_title: user.job_title || "", main_goal: user.main_goal || "", work_hours: user.work_hours || "", personalization: user.personalization || "" }); setShowProfile(true); }}>Profile</button>
            <button className="btn-secondary" onClick={handleClearHistory}>Clear Chat</button>
            <button className="btn-secondary" style={{ color: "#ef4444" }} onClick={handleWipeData}>Wipe Data</button>
            <button className="btn-secondary" onClick={handleLogout}>Logout</button>
          </div>
        </header>

        <div className="chat-layout">
          <aside className="glass-card sidebar">
            <button className="btn-primary new-chat-btn" onClick={() => { setCurrentConvId(null); setMessages([]); setShowDraft(false); setDraftEmail(""); setCalendarDraft(null); }}>+ New Chat</button>
            <div style={{ marginTop: 16 }}>
              <p className="sidebar-label">Recent Chats</p>
              {conversations.map(c => (
                <button key={c.id} className={`history-item${c.id === currentConvId ? " active" : ""}`} onClick={() => switchConv(c.id)}>{c.title}</button>
              ))}
              {conversations.length === 0 && <p style={{ fontSize: "0.8rem", opacity: 0.4, textAlign: "center", marginTop: 16 }}>No history yet</p>}
            </div>
          </aside>

          <main className="messages-area glass-card">
            {messages.length === 0 && !sending && (
              <div style={{ textAlign: "center", marginTop: 80, opacity: 0.5 }}>
                <div style={{ fontSize: "2.5rem", marginBottom: 12 }}>👋</div>
                <h3>How can I help you today?</h3>
                <p style={{ marginTop: 8, fontSize: "0.875rem" }}>Ask about emails, calendar, or ask me to remember something.</p>
              </div>
            )}
            {messages.map((m, i) => (
              <div key={i} className={`message-bubble message-${m.role}`}>
                <div style={{ fontWeight: 600, fontSize: "0.7rem", marginBottom: 4, opacity: 0.7 }}>{m.role === "user" ? "YOU" : "DESKPILOT"}</div>
                <div className="markdown-content">
                  <ReactMarkdown remarkPlugins={[remarkGfm]}>{m.content}</ReactMarkdown>
                </div>
              </div>
            ))}
            {sending && <div className="typing-indicator"><div className="dot" /><div className="dot" /><div className="dot" /></div>}

            {showDraft && !sending && (
              <div className="draft-card animate-slide-up" style={{ border: "1px solid var(--primary)", boxShadow: "0 0 20px rgba(139,92,246,0.2)" }}>
                <div className="draft-header">
                  <div style={{ display: "flex", alignItems: "center", gap: 8 }}><div className="pulse-dot" /><span>Email Draft</span></div>
                  <div style={{ fontSize: "0.75rem", color: "var(--text-muted)" }}>Edit or ask me to change anything</div>
                </div>
                <textarea className="draft-textarea" value={draftEmail} onChange={e => setDraftEmail(e.target.value)} />
                <div className="draft-actions">
                  <button className="btn-primary" style={{ flex: 1, height: 46 }} onClick={handleSendDraft} disabled={sending}>{sending ? "Sending…" : "Send Email"}</button>
                  <button className="btn-secondary" onClick={() => { setShowDraft(false); setDraftEmail(""); }}>Discard</button>
                </div>
              </div>
            )}

            {calendarDraft && !sending && (
              <div className="draft-card animate-slide-up" style={{ border: "1px solid #10b981", boxShadow: "0 0 20px rgba(16,185,129,0.2)" }}>
                <div className="draft-header" style={{ color: "#10b981" }}>
                  <div style={{ display: "flex", alignItems: "center", gap: 8 }}><div className="pulse-dot" style={{ background: "#10b981" }} /><span>Confirm Calendar Event</span></div>
                </div>
                <div style={{ padding: "12px 16px", background: "rgba(255,255,255,0.02)", borderRadius: 8, marginBottom: 12, fontSize: "0.9rem" }}>
                  <div style={{ marginBottom: 6 }}><strong>Title:</strong> {calendarDraft.title}</div>
                  <div style={{ marginBottom: 6 }}><strong>Date:</strong> {calendarDraft.date}</div>
                  <div style={{ marginBottom: 6 }}><strong>Time:</strong> {calendarDraft.time}</div>
                  {calendarDraft.description && <div><strong>Note:</strong> {calendarDraft.description}</div>}
                </div>
                <div className="draft-actions">
                  <button className="btn-primary" style={{ flex: 1, height: 46, background: "#10b981" }} onClick={() => { sendMsg("Yes, go ahead and add it to my calendar."); setCalendarDraft(null); }}>Confirm &amp; Add to Calendar</button>
                  <button className="btn-secondary" onClick={() => setCalendarDraft(null)}>Cancel</button>
                </div>
              </div>
            )}
            <div ref={bottomRef} />
          </main>
        </div>

        {error && (
          <div className="toast-container">
            <div className="toast"><div className="toast-icon">!</div><div>{error}</div></div>
          </div>
        )}

        <footer className="input-area">
          <input className="input-field" type="text" value={message} onChange={e => setMessage(e.target.value)} onKeyDown={e => e.key === "Enter" && !e.shiftKey && !sending && sendMsg()} placeholder="Type your message…" disabled={sending} />
          <button className="btn-primary send-btn" onClick={() => sendMsg()} disabled={sending || !message.trim()}>{sending ? "…" : "Send"}</button>
        </footer>
      </div>

      {showProfile && (
        <div className="modal-overlay" onClick={() => setShowProfile(false)}>
          <div className="glass-card profile-modal animate-slide-up" onClick={e => e.stopPropagation()}>
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 24 }}>
              <h2 style={{ fontSize: "1.4rem" }}>Profile</h2>
              <button className="btn-secondary" style={{ padding: "6px 12px" }} onClick={() => setShowProfile(false)}>✕</button>
            </div>
            <div style={{ display: "flex", flexDirection: "column", gap: 18 }}>
              <div><label className="field-label">Full Name</label><input className="input-field" value={profileData.name} onChange={e => setProfileData({ ...profileData, name: e.target.value })} /></div>
              <div><label className="field-label">Position</label><select className="input-field" value={profileData.job_title} onChange={e => setProfileData({ ...profileData, job_title: e.target.value })} style={{ background: "var(--glass)" }}><option>Student</option><option>Employee</option><option>Business Owner</option><option>Freelancer</option><option>Researcher</option><option>Other</option></select></div>
              <div><label className="field-label">Personalize your AI</label><p style={{ fontSize: "0.75rem", color: "var(--text-muted)", marginBottom: 6 }}>e.g. "Keep emails concise."</p><textarea className="input-field" style={{ minHeight: 72, resize: "none" }} value={profileData.personalization} onChange={e => setProfileData({ ...profileData, personalization: e.target.value })} /></div>
              <div><label className="field-label">Main Goal</label><input className="input-field" value={profileData.main_goal} onChange={e => setProfileData({ ...profileData, main_goal: e.target.value })} /></div>
              <div><label className="field-label">Work Hours</label><input className="input-field" value={profileData.work_hours} onChange={e => setProfileData({ ...profileData, work_hours: e.target.value })} placeholder="e.g. 9am–6pm" /></div>
              <button className="btn-primary" style={{ marginTop: 8 }} onClick={handleUpdateProfile} disabled={sending}>{sending ? "Saving…" : "Save Changes"}</button>
            </div>
          </div>
        </div>
      )}
    </>
  );
}

export default function Home() {
  return (
    <Suspense fallback={<div className="center-screen"><div className="spinner" /></div>}>
      <HomeInner />
    </Suspense>
  );
}
