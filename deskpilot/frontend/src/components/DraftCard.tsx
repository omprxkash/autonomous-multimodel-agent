"use client";

interface Props {
  content: string;
}

export default function DraftCard({ content }: Props) {
  const lines = content.split("\n");
  return (
    <div className="draft-card">
      <div style={{ color: "#f59e0b", fontSize: 12, fontWeight: 600, marginBottom: 8, fontFamily: "sans-serif" }}>
        DRAFT — review before confirming
      </div>
      {lines.map((line, i) => (
        <div key={i} style={{ color: line.startsWith("---") ? "#6b7280" : "#f0f4ff" }}>
          {line}
        </div>
      ))}
    </div>
  );
}
