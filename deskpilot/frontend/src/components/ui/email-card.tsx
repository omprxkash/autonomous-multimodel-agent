"use client";

import { useState } from "react";
import { Mail, Reply } from "lucide-react";
import { EmailReplyDialog } from "@/components/EmailReplyDialog";

interface EmailCardProps {
  from: string;
  subject: string;
  snippet: string;
  index: number;
  emailId?: string;
  emailBody?: string;
  priority?: "High" | "Medium" | "Low";
}

const priorityColors: Record<string, string> = {
  high: "border-l-red-500",
  medium: "border-l-yellow-500",
  low: "border-l-blue-500",
};

export function EmailCard({
  from,
  subject,
  snippet,
  index,
  emailId,
  emailBody,
  priority,
}: EmailCardProps) {
  const [replyOpen, setReplyOpen] = useState(false);
  const borderColor = priority
    ? priorityColors[priority.toLowerCase()] ?? "border-l-primary"
    : "border-l-primary";

  return (
    <>
      <div
        className={`rounded-lg border border-white/10 border-l-4 ${borderColor} bg-white/5 backdrop-blur-md p-4 space-y-2 hover:-translate-y-1 transition-all duration-200`}
      >
        <div className="flex items-start justify-between gap-2">
          <div className="flex items-center gap-2 min-w-0">
            <div className="w-8 h-8 rounded-full bg-purple-500/20 flex items-center justify-center shrink-0">
              <Mail className="w-4 h-4 text-purple-400" />
            </div>
            <p className="text-sm font-medium truncate text-white/90">{from}</p>
          </div>
          {priority && (
            <span className="text-xs px-1.5 py-0.5 rounded bg-white/10 text-white/60 shrink-0">
              {priority}
            </span>
          )}
        </div>

        <div className="pl-10">
          <h4 className="font-semibold text-sm mb-1 text-white line-clamp-1">{subject}</h4>
          <p className="text-xs text-white/50 line-clamp-2">{snippet}</p>
        </div>

        <div className="pl-10 pt-1">
          <button
            onClick={() => setReplyOpen(true)}
            className="inline-flex items-center gap-1.5 text-xs px-3 py-1.5 rounded-lg border border-white/20 hover:border-purple-400/60 hover:bg-purple-500/10 transition-all text-white/70 hover:text-white"
          >
            <Reply className="w-3 h-3" />
            Reply
          </button>
        </div>
      </div>

      <EmailReplyDialog
        open={replyOpen}
        onOpenChange={setReplyOpen}
        emailFrom={from}
        emailSubject={subject}
        emailBody={emailBody ?? snippet}
        emailId={emailId}
      />
    </>
  );
}
