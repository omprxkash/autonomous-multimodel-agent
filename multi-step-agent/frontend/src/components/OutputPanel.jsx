import React, { useState } from "react";

const TABS = ["Draft", "Outline", "Summaries"];

export default function OutputPanel({ output, status, isActive }) {
  const [activeTab, setActiveTab] = useState("Draft");

  if (isActive && !output) {
    return (
      <div style={{ background: "#1a1a1a", border: "1px solid #2a2a2a", borderRadius: "8px", padding: "32px", textAlign: "center" }}>
        <p style={{ color: "#555", fontSize: "14px", margin: 0 }}>Pipeline running...</p>
      </div>
    );
  }

  if (!output) return null;

  return (
    <div style={{ background: "#1a1a1a", border: "1px solid #2a2a2a", borderRadius: "8px", overflow: "hidden" }}>
      <div style={{ display: "flex", borderBottom: "1px solid #2a2a2a" }}>
        {TABS.map((tab) => (
          <button
            key={tab}
            onClick={() => setActiveTab(tab)}
            style={{
              flex: 1,
              padding: "12px",
              background: "none",
              border: "none",
              borderBottom: activeTab === tab ? "2px solid #3b82f6" : "2px solid transparent",
              color: activeTab === tab ? "#e8e8e8" : "#666",
              fontSize: "13px",
              fontWeight: activeTab === tab ? 600 : 400,
              cursor: "pointer",
            }}
          >
            {tab}
          </button>
        ))}
      </div>

      <div style={{ padding: "20px" }}>
        {activeTab === "Draft" && (
          output.draft ? (
            <pre style={{ margin: 0, whiteSpace: "pre-wrap", wordBreak: "break-word", fontSize: "14px", lineHeight: "1.7", color: "#d4d4d4", fontFamily: "inherit" }}>
              {output.draft}
            </pre>
          ) : (
            <p style={{ color: "#555", fontSize: "14px", margin: 0 }}>No draft yet</p>
          )
        )}

        {activeTab === "Outline" && (
          output.outline ? (
            <pre style={{ margin: 0, whiteSpace: "pre-wrap", wordBreak: "break-word", fontSize: "14px", lineHeight: "1.7", color: "#d4d4d4", fontFamily: "inherit" }}>
              {output.outline}
            </pre>
          ) : (
            <p style={{ color: "#555", fontSize: "14px", margin: 0 }}>No outline yet</p>
          )
        )}

        {activeTab === "Summaries" && (
          output.summaries && output.summaries.length > 0 ? (
            output.summaries.map((s, i) => (
              <div key={i} style={{ marginBottom: "20px", paddingBottom: "20px", borderBottom: i < output.summaries.length - 1 ? "1px solid #222" : "none" }}>
                <p style={{ margin: "0 0 6px", fontSize: "12px", color: "#666", fontWeight: 600, textTransform: "uppercase", letterSpacing: "0.05em" }}>
                  Source {i + 1}
                </p>
                <pre style={{ margin: 0, whiteSpace: "pre-wrap", wordBreak: "break-word", fontSize: "14px", lineHeight: "1.6", color: "#d4d4d4", fontFamily: "inherit" }}>
                  {s}
                </pre>
              </div>
            ))
          ) : (
            <p style={{ color: "#555", fontSize: "14px", margin: 0 }}>No summaries yet</p>
          )
        )}
      </div>
    </div>
  );
}
