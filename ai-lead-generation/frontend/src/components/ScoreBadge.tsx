interface Props {
  score: number | null;
  size?: "sm" | "md";
}

function scoreColor(score: number): string {
  if (score >= 70) return "#22c55e";
  if (score >= 45) return "#f59e0b";
  return "#ef4444";
}

export function ScoreBadge({ score, size = "md" }: Props) {
  if (score === null) return null;
  const color = scoreColor(score);
  const px = size === "sm" ? "6px 10px" : "8px 14px";
  const fontSize = size === "sm" ? "11px" : "13px";

  return (
    <span
      style={{
        display: "inline-block",
        background: color,
        color: "#fff",
        borderRadius: "999px",
        padding: px,
        fontSize,
        fontWeight: 700,
        letterSpacing: "0.02em",
        lineHeight: 1,
        minWidth: size === "sm" ? 28 : 36,
        textAlign: "center",
      }}
    >
      {score}
    </span>
  );
}

