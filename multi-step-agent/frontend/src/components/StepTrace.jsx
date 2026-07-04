import React, { useState } from "react";

const PIPELINE_STEPS = ["planner", "search", "filter", "summarise", "outline", "draft"];

const STATUS_COLORS = {
  complete: { bg: "#14532d", text: "#4ade80", label: "complete" },
  running: { bg: "#1e3a5f", text: "#60a5fa", label: "running" },
  failed: { bg: "#450a0a", text: "#f87171", label: "failed" },
  pending: { bg: "#1c1c1c", text: "#666", label: "pending" },
};

function StepCard({ log, fallbackStep }) {
  const [open, setOpen] = useState(false);
  const step = log ? log.step : fallbackStep;
  const statusKey = log ? log.status : "pending";
  const colors = STATUS_COLORS[statusKey] || STATUS_COLORS.pending;

  return (
    <div
      style={{
        background: "#1a1a1a",
        border: "1px solid #2a2a2a",
        borderRadius: "6px",
        marginBottom: "8px",
        overflow: "hidden",
      }}
    >
      <div
        style={{ display: "flex", alignItems: "center", justifyContent: "space-between", padding: "10px 14px", cursor: log?.output ? "pointer" : "default" }}
        onClick={() => log?.output && setOpen((o) => !o)}
      >
        <span style={{ fontSize: "13px", fontWeight: 500, textTransform: "capitalize" }}>{step}</span>
        <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
          <span
            style={{
              fontSize: "11px",
              fontWeight: 600,
              padding: "2px 8px",
              borderRadius: "99px",
              background: colors.bg,
              color: colors.text,
              textTransform: "uppercase",
              letterSpacing: "0.04em",
            }}
          >
            {colors.label}
          </span>
          {log?.output && (
            <span style={{ fontSize: "11px", color: "#555" }}>{open ? "▲" : "▼"}</span>
          )}
        </div>
      </div>
      {open && log?.output && (
        <div style={{ padding: "0 14px 12px", fontSize: "12px", color: "#aaa", borderTop: "1px solid #222", paddingTop: "10px" }}>
          {log.output}
        </div>
      )}
    </div>
  );
}

export default function StepTrace({ stepLogs, status }) {
  const logMap = {};
  (stepLogs || []).forEach((l) => { logMap[l.step] = l; });

  return (
    <div style={{ background: "#1a1a1a", border: "1px solid #2a2a2a", borderRadius: "8px", padding: "20px" }}>
      <h2 style={{ margin: "0 0 14px", fontSize: "14px", fontWeight: 600, textTransform: "uppercase", letterSpacing: "0.05em", color: "#999" }}>
        Pipeline Steps
      </h2>
      {PIPELINE_STEPS.map((step) => (
        <StepCard key={step} log={logMap[step] || null} fallbackStep={step} />
      ))}
      {status === "failed" && (
        <p style={{ margin: "8px 0 0", fontSize: "12px", color: "#f87171" }}>Pipeline failed</p>
      )}
    </div>
  );
}
