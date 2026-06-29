"use client";
import { useEffect, useState } from "react";
import { listAnalyses } from "@/lib/api";
import { AnalysisSummary } from "@/lib/types";
import VerdictBadge from "@/components/VerdictBadge";

export default function Dashboard() {
  const [analyses, setAnalyses] = useState<AnalysisSummary[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    listAnalyses().then(setAnalyses).finally(() => setLoading(false));
  }, []);

  return (
    <div>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 24 }}>
        <div>
          <h1 style={{ fontSize: 24, fontWeight: 700 }}>Investigations</h1>
          <p style={{ color: "var(--muted)", marginTop: 4 }}>Recent email and URL analyses</p>
        </div>
        <a href="/submit" className="btn btn-primary">+ New Analysis</a>
      </div>

      {loading ? (
        <p style={{ color: "var(--muted)" }}>Loading...</p>
      ) : analyses.length === 0 ? (
        <div className="card" style={{ textAlign: "center", padding: 48 }}>
          <p style={{ color: "var(--muted)" }}>No analyses yet.</p>
          <a href="/submit" className="btn btn-primary" style={{ marginTop: 16 }}>Submit your first sample</a>
        </div>
      ) : (
        <div className="card" style={{ padding: 0, overflow: "hidden" }}>
          <table style={{ width: "100%", borderCollapse: "collapse" }}>
            <thead>
              <tr style={{ borderBottom: "1px solid var(--border)" }}>
                {["Type", "Target", "Score", "Verdict", "Status", "Date", ""].map((h) => (
                  <th key={h} style={{ padding: "12px 16px", textAlign: "left", color: "var(--muted)", fontWeight: 500, fontSize: 12 }}>{h}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {analyses.map((a) => (
                <tr key={a.analysis_id} style={{ borderBottom: "1px solid var(--border)" }}>
                  <td style={{ padding: "12px 16px" }}>
                    <span style={{ background: "var(--border)", padding: "2px 8px", borderRadius: 4, fontSize: 11, fontWeight: 600, textTransform: "uppercase" }}>{a.type}</span>
                  </td>
                  <td style={{ padding: "12px 16px", maxWidth: 200, overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>{a.target}</td>
                  <td style={{ padding: "12px 16px", fontWeight: 700 }}>{a.score ?? "—"}</td>
                  <td style={{ padding: "12px 16px" }}>{a.verdict ? <VerdictBadge verdict={a.verdict} /> : "—"}</td>
                  <td style={{ padding: "12px 16px", color: "var(--muted)" }}>{a.status}</td>
                  <td style={{ padding: "12px 16px", color: "var(--muted)" }}>{new Date(a.created_at).toLocaleDateString()}</td>
                  <td style={{ padding: "12px 16px" }}>
                    {a.status === "complete" && <a href={`/report/${a.analysis_id}`} style={{ color: "var(--accent)" }}>View →</a>}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
