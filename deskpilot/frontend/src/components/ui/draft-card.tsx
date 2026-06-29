"use client";

import { useState } from "react";
import { PenSquare, Send } from "lucide-react";
import { ComposeEmailDialog } from "@/components/ComposeEmailDialog";

interface DraftCardProps {
  to: string;
  subject: string;
  body: string;
}

export function DraftCard({ to, subject, body }: DraftCardProps) {
  const [open, setOpen] = useState(false);

  return (
    <>
      <div className="rounded-lg border border-purple-400/30 border-l-4 border-l-purple-500 bg-purple-500/5 backdrop-blur-md p-4 space-y-3 hover:-translate-y-1 transition-all duration-200">
        <div className="flex items-start justify-between gap-4">
          <div className="space-y-2 flex-1 min-w-0">
            <div className="flex items-center gap-2 text-purple-400">
              <PenSquare className="w-4 h-4" />
              <span className="font-semibold text-sm">Draft Ready</span>
            </div>

            <div className="grid gap-1 text-sm">
              <div className="flex gap-2">
                <span className="text-white/40 w-10 shrink-0">To:</span>
                <span className="font-medium text-white truncate">{to}</span>
              </div>
              <div className="flex gap-2">
                <span className="text-white/40 w-10 shrink-0">Subj:</span>
                <span className="font-medium text-white truncate">{subject}</span>
              </div>
            </div>

            <div className="text-xs text-white/40 line-clamp-2 bg-white/5 p-2.5 rounded-lg font-mono border border-white/10">
              {body}
            </div>
          </div>

          <button
            onClick={() => setOpen(true)}
            className="inline-flex items-center gap-1.5 text-xs px-3 py-1.5 rounded-lg bg-purple-600 hover:bg-purple-500 text-white transition-all shrink-0"
          >
            <Send className="w-3 h-3" />
            Review & Send
          </button>
        </div>
      </div>

      <ComposeEmailDialog
        open={open}
        onOpenChange={setOpen}
        initialTo={to}
        initialSubject={subject}
        initialBody={body}
      />
    </>
  );
}
