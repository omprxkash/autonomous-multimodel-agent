const STAGES = [
  "Email Parsing",
  "Header Forensics",
  "Auth Verification",
  "URL Analysis",
  "Domain Intelligence",
  "Threat Intel",
  "NLP Detection",
  "Risk Scoring",
  "Report Generation",
];

export default function PipelineStatus({ status }: { status: string }) {
  const running = status === "running";
  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
      {STAGES.map((stage, i) => (
        <div key={stage} style={{ display: "flex", alignItems: "center", gap: 12 }}>
          <div style={{
            width: 8, height: 8, borderRadius: "50%",
            background: running ? "var(--accent)" : "var(--border)",
            animation: running ? "pulse 1.2s infinite" : "none",
            animationDelay: `${i * 0.1}s`,
          }} />
          <span style={{ color: "var(--muted)", fontSize: 13 }}>{stage}</span>
        </div>
      ))}
      <style>{`@keyframes pulse { 0%,100%{opacity:1} 50%{opacity:0.3} }`}</style>
    </div>
  );
}
