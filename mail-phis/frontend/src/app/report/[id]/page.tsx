"use client";
import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { getReport, pollStatus, exportUrl } from "@/lib/api";
import { Report, AnalysisSummary } from "@/lib/types";
import VerdictBadge from "@/components/VerdictBadge";
import FeatureBreakdown from "@/components/FeatureBreakdown";
import PipelineStatus from "@/components/PipelineStatus";

export default function ReportPage() {
  const { id } = useParams<{ id: string }>();
  const [report, setReport] = useState<Report | null>(null);
  const [status, setStatus] = useState<AnalysisSummary | null>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    let timer: ReturnType<typeof setInterval>;

    async function poll() {
      try {
        const s = await pollStatus(id);
        setStatus(s);
        if (s.status === "complete") {
          clearInterval(timer);
          const r = await getReport(id);
          setReport(r);
        } else if (s.status === "failed") {
          clearInterval(timer);
          setError("Analysis failed.");
        }
      } catch {
        clearInterval(timer);
        setError("Could not load analysis.");
      }
    }

    poll();
    timer = setInterval(poll, 2500);
    return () => clearInterval(timer);
  }, [id]);

  if (error) return <p style={{ color: "var(--phishing)" }}>{error}</p>;

  if (!report) {
    return (
      <div>
        <h2 style={{ marginBottom: 12 }}>Analyzing…</h2>
        <p style={{ color: "var(--muted)" }}>Status: {status?.status ?? "pending"}</p>
        <div style={{ marginTop: 24 }}>
          <PipelineStatus status={status?.status ?? "pending"} />
        </div>
      </div>
    );
  }

  const verdorColor: Record<string, string> = {
    SAFE: "var(--safe)", MARKETING: "var(--marketing)",
    SUSPICIOUS: "var(--suspicious)", PHISHING: "var(--phishing)",
  };

  return (
    <div>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: 24 }}>
        <div>
          <h1 style={{ fontSize: 22, fontWeight: 700, marginBottom: 6 }}>
            {report.type === "email" ? "Email" : "URL"} Report
          </h1>
          <p style={{ color: "var(--muted)", fontSize: 13, wordBreak: "break-all" }}>{report.target}</p>
        </div>
        <div style={{ display: "flex", gap: 8 }}>
          {(["json", "csv", "stix2"] as const).map((fmt) => (
            <a key={fmt} href={exportUrl(id, fmt)} className="btn btn-outline" style={{ fontSize: 12 }}>
              Export {fmt.toUpperCase()}
            </a>
          ))}
        </div>
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr 1fr", gap: 16, marginBottom: 24 }}>
        <div className="card" style={{ textAlign: "center" }}>
          <div className="score-ring" style={{ margin: "0 auto 12px", borderColor: verdorColor[report.verdict] }}>
            {report.score}
          </div>
          <VerdictBadge verdict={report.verdict} />
        </div>
        <div className="card">
          <p style={{ color: "var(--muted)", fontSize: 12, marginBottom: 8 }}>IOCs Extracted</p>
          <p><strong>{report.iocs.ips.length}</strong> IPs</p>
          <p><strong>{report.iocs.domains.length}</strong> Domains</p>
          <p><strong>{report.iocs.urls.length}</strong> URLs</p>
          <p><strong>{report.iocs.emails.length}</strong> Emails</p>
        </div>
        <div className="card">
          <p style={{ color: "var(--muted)", fontSize: 12, marginBottom: 8 }}>Analysis ID</p>
          <p style={{ fontFamily: "monospace", fontSize: 11, wordBreak: "break-all" }}>{report.analysis_id}</p>
          <p style={{ color: "var(--muted)", fontSize: 12, marginTop: 12 }}>Completed</p>
          <p style={{ fontSize: 12 }}>{new Date(report.completed_at).toLocaleString()}</p>
        </div>
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16 }}>
        <div className="card">
          <h3 style={{ marginBottom: 16, fontSize: 15 }}>Top Risk Factors</h3>
          <FeatureBreakdown features={report.top_features} verdict={report.verdict} />
        </div>
        <div className="card">
          <h3 style={{ marginBottom: 16, fontSize: 15 }}>Indicators of Compromise</h3>
          {Object.entries(report.iocs).map(([type, values]) =>
            values.length > 0 ? (
              <div key={type} style={{ marginBottom: 12 }}>
                <p style={{ fontSize: 11, color: "var(--muted)", textTransform: "uppercase", marginBottom: 4 }}>{type}</p>
                {values.map((v) => (
                  <p key={v} style={{ fontFamily: "monospace", fontSize: 12, padding: "3px 0", borderBottom: "1px solid var(--border)" }}>{v}</p>
                ))}
              </div>
            ) : null
          )}
        </div>
      </div>
    </div>
  );
}
