import { DragDropContext, Droppable, type DropResult } from "@hello-pangea/dnd";
import type { Lead } from "../api/client";
import { LeadCard } from "./LeadCard";

const STAGES = [
  { id: "new", label: "New" },
  { id: "enriched", label: "Enriched" },
  { id: "scored", label: "Scored" },
  { id: "contacted", label: "Contacted" },
  { id: "replied", label: "Replied" },
  { id: "won", label: "Won" },
  { id: "lost", label: "Lost" },
];

const STAGE_COLORS: Record<string, string> = {
  new: "#e0f2fe",
  enriched: "#fef3c7",
  scored: "#ede9fe",
  contacted: "#d1fae5",
  replied: "#dbeafe",
  won: "#dcfce7",
  lost: "#fee2e2",
};

interface Props {
  leads: Lead[];
  onDragEnd: (result: DropResult) => void;
  onCardClick: (lead: Lead) => void;
}

export function KanbanBoard({ leads, onDragEnd, onCardClick }: Props) {
  const byStage = (stage: string) => leads.filter((l) => l.stage === stage);

  return (
    <DragDropContext onDragEnd={onDragEnd}>
      <div
        style={{
          display: "flex",
          gap: 12,
          overflowX: "auto",
          padding: "0 4px 16px",
          minHeight: "calc(100vh - 100px)",
        }}
      >
        {STAGES.map((stage) => {
          const stageLeads = byStage(stage.id);
          return (
            <div
              key={stage.id}
              style={{
                flex: "0 0 220px",
                display: "flex",
                flexDirection: "column",
              }}
            >
              <div
                style={{
                  display: "flex",
                  alignItems: "center",
                  gap: 8,
                  marginBottom: 10,
                  padding: "6px 10px",
                  background: STAGE_COLORS[stage.id] ?? "#f3f4f6",
                  borderRadius: 8,
                }}
              >
                <span style={{ fontWeight: 700, fontSize: 13, color: "#374151" }}>
                  {stage.label}
                </span>
                <span
                  style={{
                    marginLeft: "auto",
                    background: "rgba(0,0,0,0.08)",
                    borderRadius: 999,
                    padding: "1px 7px",
                    fontSize: 11,
                    color: "#374151",
                    fontWeight: 600,
                  }}
                >
                  {stageLeads.length}
                </span>
              </div>
              <Droppable droppableId={stage.id}>
                {(provided, snapshot) => (
                  <div
                    ref={provided.innerRef}
                    {...provided.droppableProps}
                    style={{
                      flex: 1,
                      minHeight: 60,
                      background: snapshot.isDraggingOver ? "#f0fdf4" : "transparent",
                      borderRadius: 8,
                      transition: "background 0.15s",
                      padding: 4,
                    }}
                  >
                    {stageLeads.map((lead, index) => (
                      <LeadCard
                        key={lead.id}
                        lead={lead}
                        index={index}
                        onClick={onCardClick}
                      />
                    ))}
                    {provided.placeholder}
                  </div>
                )}
              </Droppable>
            </div>
          );
        })}
      </div>
    </DragDropContext>
  );
}

