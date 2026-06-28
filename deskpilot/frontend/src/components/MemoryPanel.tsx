"use client";

import { useEffect, useState } from "react";

interface MemoryFact {
  id: string;
  category: string;
  content: string;
  importance: number;
}

export default function MemoryPanel() {
  const [facts, setFacts] = useState<MemoryFact[]>([]);
  const [open, setOpen] = useState(false);

  useEffect(() => {
    if (!open) return;
    const token = localStorage.getItem("dp_token");
    fetch("/api/chat/memories", { headers: { Authorization: `Bearer ${token}` } })
      .then((r) => r.json())
      .then(setFacts)
      .catch(() => {});
  }, [open]);

  return (
    <div>
      <button
        onClick={() => setOpen((p) => !p)}
        style={{
          background: "none",
          border: "none",
          color: "var(--muted)",
          cursor: "pointer",
          padding: "8px 12px",
          fontSize: 13,
          display: "flex",
          alignItems: "center",
          gap: 6,
          width: "100%",
          borderRadius: 8,
        }}
      >
        <span>{open ? "▾" : "▸"}</span> Memory ({facts.length})
      </button>
      {open && (
        <div style={{ padding: "0 8px 8px" }}>
          {facts.length === 0 ? (
            <div style={{ color: "var(--muted)", fontSize: 12, padding: "4px 8px" }}>No memories yet</div>
          ) : (
            facts.map((f) => (
              <div
                key={f.id}
                style={{
                  background: "var(--glass)",
                  border: "1px solid var(--glass-border)",
                  borderRadius: 8,
                  padding: "8px 10px",
                  marginBottom: 6,
                  fontSize: 12,
                  color: "var(--text)",
                }}
              >
                <div style={{ color: "var(--accent-light)", fontSize: 11, marginBottom: 2 }}>{f.category}</div>
                {f.content}
              </div>
            ))
          )}
        </div>
      )}
    </div>
  );
}
