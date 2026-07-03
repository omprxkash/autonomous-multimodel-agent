import { Draggable } from "@hello-pangea/dnd";
import type { Lead } from "../api/client";
import { ScoreBadge } from "./ScoreBadge";

interface Props {
  lead: Lead;
  index: number;
  onClick: (lead: Lead) => void;
}

export function LeadCard({ lead, index, onClick }: Props) {
  return (
    <Draggable draggableId={lead.id} index={index}>
      {(provided, snapshot) => (
        <div
          ref={provided.innerRef}
          {...provided.draggableProps}
          {...provided.dragHandleProps}
          onClick={() => onClick(lead)}
          style={{
            background: snapshot.isDragging ? "#e0f2fe" : "#fff",
            borderRadius: 10,
            padding: "12px 14px",
            marginBottom: 8,
            boxShadow: snapshot.isDragging
              ? "0 4px 16px rgba(0,0,0,0.15)"
              : "0 1px 4px rgba(0,0,0,0.08)",
            cursor: "grab",
            border: "1px solid #e5e7eb",
            transition: "box-shadow 0.15s",
            ...provided.draggableProps.style,
          }}
        >
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", gap: 8 }}>
            <div style={{ minWidth: 0 }}>
              <div style={{ fontWeight: 600, fontSize: 14, color: "#111", marginBottom: 2, whiteSpace: "nowrap", overflow: "hidden", textOverflow: "ellipsis" }}>
                {lead.company}
              </div>
              <div style={{ fontSize: 12, color: "#6b7280", marginBottom: 4 }}>
                {lead.contact_name} · {lead.title}
              </div>
              {lead.industry && (
                <div style={{ fontSize: 11, color: "#9ca3af", textTransform: "capitalize" }}>
                  {lead.industry}
                </div>
              )}
            </div>
            <ScoreBadge score={lead.score} size="sm" />
          </div>
          {lead.tech_stack?.length > 0 && (
            <div style={{ marginTop: 8, display: "flex", flexWrap: "wrap", gap: 4 }}>
              {lead.tech_stack.slice(0, 4).map((t) => (
                <span
                  key={t}
                  style={{
                    background: "#f3f4f6",
                    borderRadius: 4,
                    padding: "2px 6px",
                    fontSize: 10,
                    color: "#374151",
                  }}
                >
                  {t}
                </span>
              ))}
            </div>
          )}
        </div>
      )}
    </Draggable>
  );
}

