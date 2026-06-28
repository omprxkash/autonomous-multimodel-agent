"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { getMe } from "@/lib/api";
import { clearToken, isAuthenticated } from "@/lib/auth";
import { User } from "@/lib/types";

export default function ProfilePage() {
  const router = useRouter();
  const [user, setUser] = useState<User | null>(null);
  const [personalization, setPersonalization] = useState("");
  const [saved, setSaved] = useState(false);

  useEffect(() => {
    if (!isAuthenticated()) { router.replace("/"); return; }
    getMe().then((u) => { setUser(u); setPersonalization(u.personalization); }).catch(() => router.replace("/"));
  }, [router]);

  async function savePersonalization() {
    const token = localStorage.getItem("dp_token");
    await fetch("/api/auth/personalization", {
      method: "PATCH",
      headers: { "Content-Type": "application/json", Authorization: `Bearer ${token}` },
      body: JSON.stringify({ personalization }),
    });
    setSaved(true);
    setTimeout(() => setSaved(false), 2000);
  }

  function logout() {
    clearToken();
    router.push("/");
  }

  if (!user) return null;

  return (
    <div style={{ maxWidth: 520, margin: "60px auto", padding: "0 24px" }}>
      <button
        style={{ background: "none", border: "none", color: "var(--muted)", cursor: "pointer", marginBottom: 24, fontSize: 13 }}
        onClick={() => router.push("/")}
      >
        ← Back
      </button>

      <div style={{ display: "flex", alignItems: "center", gap: 16, marginBottom: 32 }}>
        {user.picture && (
          <img src={user.picture} alt="" style={{ width: 56, height: 56, borderRadius: "50%" }} />
        )}
        <div>
          <div style={{ fontSize: 18, fontWeight: 600 }}>{user.name}</div>
          <div style={{ color: "var(--muted)", fontSize: 13 }}>{user.email}</div>
        </div>
      </div>

      <div
        style={{
          background: "var(--glass)",
          border: "1px solid var(--glass-border)",
          borderRadius: 16,
          padding: 24,
          marginBottom: 16,
        }}
      >
        <label style={{ fontSize: 13, color: "var(--muted)", display: "block", marginBottom: 8 }}>
          Agent behaviour
        </label>
        <textarea
          rows={4}
          value={personalization}
          onChange={(e) => setPersonalization(e.target.value)}
          style={{
            width: "100%",
            background: "var(--glass)",
            border: "1px solid var(--glass-border)",
            borderRadius: 10,
            padding: "10px 14px",
            color: "var(--text)",
            fontSize: 14,
            resize: "vertical",
            outline: "none",
            fontFamily: "inherit",
            lineHeight: 1.6,
          }}
          placeholder="e.g. Be concise. Always use bullet points for lists. Prefer morning calendar slots."
        />
        <div style={{ marginTop: 12, display: "flex", gap: 10, alignItems: "center" }}>
          <button className="btn btn-primary" onClick={savePersonalization}>
            Save
          </button>
          {saved && <span style={{ color: "var(--accent-light)", fontSize: 13 }}>Saved!</span>}
        </div>
      </div>

      <button className="btn btn-outline" onClick={logout}>
        Sign out
      </button>
    </div>
  );
}
