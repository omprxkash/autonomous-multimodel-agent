import { Feature, Verdict } from "@/lib/types";

const verdictColor: Record<Verdict, string> = {
  SAFE: "var(--safe)",
  MARKETING: "var(--marketing)",
  SUSPICIOUS: "var(--suspicious)",
  PHISHING: "var(--phishing)",
};

export default function FeatureBreakdown({ features, verdict }: { features: Feature[]; verdict: Verdict }) {
  const max = Math.max(...features.map((f) => Math.abs(f.weight)), 1);
  const color = verdictColor[verdict];

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
      {features.map(({ feature, weight }) => (
        <div key={feature}>
          <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 4 }}>
            <span style={{ fontSize: 12, color: "var(--muted)", textTransform: "capitalize" }}>
              {feature.replace(/_/g, " ")}
            </span>
            <span style={{ fontSize: 12, fontWeight: 600 }}>{weight.toFixed(1)}</span>
          </div>
          <div style={{ background: "var(--border)", borderRadius: 4, height: 6 }}>
            <div style={{
              height: 6,
              borderRadius: 4,
              background: color,
              width: `${(Math.abs(weight) / max) * 100}%`,
              transition: "width 0.4s ease",
            }} />
          </div>
        </div>
      ))}
    </div>
  );
}
