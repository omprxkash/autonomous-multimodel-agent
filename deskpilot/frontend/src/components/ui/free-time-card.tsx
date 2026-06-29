import { Clock, Calendar } from "lucide-react";

interface FreeTimeSlot {
  start: string;
  end: string;
  duration: string;
}

interface FreeTimeCardProps {
  date: string;
  slots: FreeTimeSlot[];
}

export function FreeTimeCard({ date, slots }: FreeTimeCardProps) {
  return (
    <div className="rounded-lg border border-white/10 bg-white/5 backdrop-blur-md p-4 space-y-3">
      <div className="flex items-center gap-2">
        <div className="w-10 h-10 rounded-full bg-green-500/10 flex items-center justify-center">
          <Calendar className="w-5 h-5 text-green-400" />
        </div>
        <div>
          <p className="font-semibold text-sm text-white">Free Time Slots</p>
          <p className="text-xs text-white/40">{date}</p>
        </div>
      </div>

      <div className="space-y-2">
        {slots.map((slot, i) => (
          <div
            key={i}
            className="flex items-center justify-between p-2.5 rounded-lg bg-white/5 border border-white/10 hover:border-green-400/40 transition-colors"
          >
            <div className="flex items-center gap-2">
              <Clock className="w-4 h-4 text-green-400" />
              <span className="text-sm font-medium text-white">
                {slot.start} – {slot.end}
              </span>
            </div>
            <span className="text-xs px-2 py-0.5 rounded bg-green-500/10 text-green-400 border border-green-500/20">
              {slot.duration}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}
