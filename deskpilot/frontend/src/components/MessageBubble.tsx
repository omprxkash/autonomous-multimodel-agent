"use client";

import DraftCard from "./DraftCard";
import { Message } from "@/lib/types";

interface Props {
  message: Message;
}

const DRAFT_MARKER = "--- DRAFT START ---";

function parseContent(content: string) {
  const idx = content.indexOf(DRAFT_MARKER);
  if (idx === -1) return { text: content, draft: null };
  return {
    text: content.slice(0, idx).trim(),
    draft: content.slice(idx).trim(),
  };
}

export default function MessageBubble({ message }: Props) {
  const { text, draft } = parseContent(message.content);
  return (
    <div>
      <div className={`bubble ${message.role}`}>{text}</div>
      {draft && <DraftCard content={draft} />}
    </div>
  );
}
