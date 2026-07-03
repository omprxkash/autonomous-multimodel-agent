import type { Lead, FactorBreakdown } from "../api/client";
import { ScoreBadge } from "./ScoreBadge";

interface Props {
  lead: Lead | null;
  onClose: () => void;
}

function FactorRow({ name, factor }: { name: string; factor: FactorBreakdown }) {
  const pct = Math.round((factor.points / factor.max) * 100);
  return (
    <div style={{ marginBottom: 12 }}>
      <div style={{ display: "flex", justifyContent: "space-between", fontSize: 13, marginBottom: 4 }}>
        <span style={{ color: "#374151", textTransform: "capitalize" }}>{name.replace("_", " ")}</span>
        <span style={{ fontWeight: 600, color: factor.points > 0 ? "#22c55e" : "#9ca3af" }}>
          {factor.points}/{factor.max}
        </span>
      </div>
      <div style={{ height: 6, background: "#f3f4f6", borderRadius: 4, overflow: "hidden" }}>
        <div
          style={{
            width: `${pct}%`,
            height: "100%",
            background: pct >= 70 ? "#22c55e" : pct >= 40 ? "#f59e0b" : "#ef4444",
            borderRadius: 4,
            transition: "width 0.3s",
          }}
        />
      </div>
      {factor.matched !== undefined && (
        <div style={{ fontSize: 11, color: "#9ca3af", marginTop: 2 }}>
          {Array.isArray(factor.matched)
            ? `Matched: ${factor.matched.join(", ") || "none"}`
            : factor.matched
            ? "✓ Match"
            : "✗ No match"}
        </div>
      )}
    </div>
  );
}

export function LeadDrawer({ lead, onClose }: Props) {
  if (!lead) return null;

  return (
    <>
      <div
        onClick={onClose}
        style={{
          position: "fixed", inset: 0, background: "rgba(0,0,0,0.3)", zIndex: 40,
        }}
      />
      <div
        style={{
          position: "fixed", right: 0, top: 0, bottom: 0, width: 440,
          background: "#fff", zIndex: 50, overflowY: "auto",
          boxShadow: "-4px 0 24px rgba(0,0,0,0.12)",
          padding: 28,
        }}
      >
        <button
          onClick={onClose}
          style={{ position: "absolute", top: 16, right: 16, background: "none", border: "none", fontSize: 20, cursor: "pointer", color: "#6b7280" }}
        >
          ✕
        </button>

        <div style={{ display: "flex", alignItems: "center", gap: 12, marginBottom: 20 }}>
          <div>
            <h2 style={{ fontSize: 20, fontWeight: 700, color: "#111", margin: 0 }}>{lead.company}</h2>
            <div style={{ fontSize: 13, color: "#6b7280" }}>{lead.domain}</div>
          </div>
          <ScoreBadge score={lead.score} />
        </div>

        <Section title="Contact">
          <Row label="Name" value={lead.contact_name} />
          <Row label="Title" value={lead.title} />
          <Row label="Email" value={lead.email} />
        </Section>

        <Section title="Company">
          <Row label="Industry" value={lead.industry} />
          <Row label="Employees" value={lead.employee_count?.toString()} />
          <Row label="Location" value={lead.location} />
          {lead.tech_stack?.length > 0 && (
            <Row label="Tech" value={lead.tech_stack.join(", ")} />
          )}
        </Section>

        {lead.score_breakdown && (
          <Section title="Score Breakdown">
            {Object.entries(lead.score_breakdown).map(([key, factor]) => (
              <FactorRow key={key} name={key} factor={factor as FactorBreakdown} />
            ))}
          </Section>
        )}

        {lead.email_draft && (
          <Section title="Outreach Draft">
            <pre
              style={{
                background: "#f9fafb", borderRadius: 8, padding: 16,
                fontSize: 12, whiteSpace: "pre-wrap", lineHeight: 1.6,
                color: "#374151", border: "1px solid #e5e7eb", margin: 0,
              }}
            >
              {lead.email_draft}
            </pre>
          </Section>
        )}
      </div>
    </>
  );
}

function Section({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <div style={{ marginBottom: 24 }}>
      <h3 style={{ fontSize: 12, fontWeight: 700, textTransform: "uppercase", letterSpacing: "0.08em", color: "#9ca3af", marginBottom: 10 }}>
        {title}
      </h3>
      {children}
    </div>
  );
}

function Row({ label, value }: { label: string; value: string | null | undefined }) {
  if (!value) return null;
  return (
    <div style={{ display: "flex", gap: 8, marginBottom: 6, fontSize: 13 }}>
      <span style={{ color: "#9ca3af", minWidth: 80 }}>{label}</span>
      <span style={{ color: "#111" }}>{value}</span>
    </div>
  );
}


