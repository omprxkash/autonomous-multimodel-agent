import { useState, useEffect, useCallback } from "react";
import type { DropResult } from "@hello-pangea/dnd";
import { api, type Lead } from "./api/client";
import { KanbanBoard } from "./components/KanbanBoard";
import { LeadDrawer } from "./components/LeadDrawer";

export default function App() {
  const [leads, setLeads] = useState<Lead[]>([]);
  const [selected, setSelected] = useState<Lead | null>(null);
  const [loading, setLoading] = useState(false);
  const [running, setRunning] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchLeads = useCallback(async () => {
    setLoading(true);
    try {
      const data = await api.getLeads();
      setLeads(data);
    } catch (e) {
      setError(String(e));
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchLeads();
  }, [fetchLeads]);

  const handleRunPipeline = async () => {
    setRunning(true);
    setError(null);
    try {
      await api.runPipeline(true);
      await fetchLeads();
    } catch (e) {
      setError(String(e));
    } finally {
      setRunning(false);
    }
  };

  const handleDragEnd = async (result: DropResult) => {
    if (!result.destination) return;
    const newStage = result.destination.droppableId;
    const leadId = result.draggableId;
    if (result.source.droppableId === newStage) return;

    setLeads((prev) =>
      prev.map((l) => (l.id === leadId ? { ...l, stage: newStage } : l))
    );

    try {
      await api.updateStage(leadId, newStage);
    } catch {
      await fetchLeads();
    }
  };

  return (
    <div style={{ minHeight: "100vh", background: "#f0f2f5" }}>
      <header
        style={{
          background: "#1e293b",
          color: "#fff",
          padding: "14px 24px",
          display: "flex",
          alignItems: "center",
          gap: 16,
          boxShadow: "0 2px 8px rgba(0,0,0,0.15)",
        }}
      >
        <div>
          <div style={{ fontWeight: 800, fontSize: 18, letterSpacing: "-0.01em" }}>
            Lead Pipeline
          </div>
          <div style={{ fontSize: 12, color: "#94a3b8", marginTop: 1 }}>
            {leads.length} lead{leads.length !== 1 ? "s" : ""} loaded
          </div>
        </div>
        <div style={{ marginLeft: "auto", display: "flex", gap: 10, alignItems: "center" }}>
          {error && (
            <span style={{ fontSize: 12, color: "#fca5a5", maxWidth: 260, overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>
              {error}
            </span>
          )}
          <button
            onClick={handleRunPipeline}
            disabled={running}
            style={{
              background: running ? "#334155" : "#3b82f6",
              color: "#fff",
              border: "none",
              borderRadius: 8,
              padding: "8px 18px",
              fontWeight: 600,
              fontSize: 13,
              cursor: running ? "not-allowed" : "pointer",
              transition: "background 0.15s",
            }}
          >
            {running ? "Running…" : "Run Pipeline"}
          </button>
          <button
            onClick={fetchLeads}
            disabled={loading}
            style={{
              background: "transparent",
              color: "#94a3b8",
              border: "1px solid #334155",
              borderRadius: 8,
              padding: "8px 14px",
              fontWeight: 600,
              fontSize: 13,
              cursor: loading ? "not-allowed" : "pointer",
            }}
          >
            {loading ? "…" : "Refresh"}
          </button>
        </div>
      </header>

      <main style={{ padding: "20px 20px 0" }}>
        {leads.length === 0 && !loading ? (
          <div
            style={{
              textAlign: "center",
              marginTop: 80,
              color: "#6b7280",
            }}
          >
            <div style={{ fontSize: 32, marginBottom: 12 }}>📋</div>
            <div style={{ fontWeight: 600, fontSize: 16, marginBottom: 6 }}>No leads yet</div>
            <div style={{ fontSize: 14 }}>Hit "Run Pipeline" to scrape and score mock companies.</div>
          </div>
        ) : (
          <KanbanBoard
            leads={leads}
            onDragEnd={handleDragEnd}
            onCardClick={setSelected}
          />
        )}
      </main>

      <LeadDrawer lead={selected} onClose={() => setSelected(null)} />
    </div>
  );
}


