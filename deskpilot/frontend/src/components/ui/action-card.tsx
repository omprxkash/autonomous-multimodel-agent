import {
  CheckCircle2,
  Forward,
  Trash2,
  Archive,
  Star,
  Mail,
  Calendar,
} from "lucide-react";

type ActionType =
  | "forward"
  | "delete"
  | "archive"
  | "star"
  | "send"
  | "create"
  | "move"
  | "success";

interface ActionCardProps {
  type: ActionType;
  title: string;
  details?: string;
}

const iconMap: Record<ActionType, { Icon: typeof CheckCircle2; color: string; bg: string }> = {
  forward: { Icon: Forward, color: "text-blue-400", bg: "bg-blue-500/10" },
  delete: { Icon: Trash2, color: "text-red-400", bg: "bg-red-500/10" },
  archive: { Icon: Archive, color: "text-amber-400", bg: "bg-amber-500/10" },
  star: { Icon: Star, color: "text-yellow-400", bg: "bg-yellow-500/10" },
  send: { Icon: Mail, color: "text-green-400", bg: "bg-green-500/10" },
  create: { Icon: Calendar, color: "text-purple-400", bg: "bg-purple-500/10" },
  move: { Icon: Calendar, color: "text-indigo-400", bg: "bg-indigo-500/10" },
  success: { Icon: CheckCircle2, color: "text-green-400", bg: "bg-green-500/10" },
};

export function ActionCard({ type, title, details }: ActionCardProps) {
  const { Icon, color, bg } = iconMap[type] ?? iconMap.success;

  return (
    <div className="rounded-lg border border-white/10 bg-white/5 backdrop-blur-md p-4">
      <div className="flex items-start gap-3">
        <div className={`w-10 h-10 rounded-full flex items-center justify-center shrink-0 ${bg}`}>
          <Icon className={`w-5 h-5 ${color}`} />
        </div>
        <div className="flex-1 min-w-0">
          <p className="font-semibold text-sm text-white">{title}</p>
          {details && (
            <p className="text-xs text-white/50 mt-1 line-clamp-2">{details}</p>
          )}
        </div>
        <CheckCircle2 className="w-5 h-5 text-green-400 shrink-0" />
      </div>
    </div>
  );
}
