import { Calendar, Clock, MapPin, Users } from "lucide-react";

interface EventCardProps {
  title: string;
  start: string;
  end?: string;
  location?: string;
  attendees?: string[];
}

export function EventCard({ title, start, end, location, attendees }: EventCardProps) {
  return (
    <div className="rounded-lg border border-white/10 border-l-4 border-l-purple-500 bg-white/5 backdrop-blur-md p-4 space-y-3 hover:-translate-y-1 transition-all duration-200">
      <div className="flex items-start gap-3">
        <div className="w-10 h-10 rounded-lg bg-purple-500/20 flex items-center justify-center shrink-0">
          <Calendar className="w-5 h-5 text-purple-400" />
        </div>
        <div className="flex-1 min-w-0">
          <h4 className="font-semibold text-white mb-1">{title}</h4>
          <div className="flex items-center gap-1 text-xs text-white/50">
            <Clock className="w-3 h-3" />
            <span>{start}</span>
            {end && <span>– {end}</span>}
          </div>
        </div>
      </div>

      {(location || (attendees && attendees.length > 0)) && (
        <div className="pl-13 space-y-1 text-xs">
          {location && (
            <div className="flex items-center gap-1 text-white/50">
              <MapPin className="w-3 h-3" />
              <span>{location}</span>
            </div>
          )}
          {attendees && attendees.length > 0 && (
            <div className="flex items-center gap-1">
              <Users className="w-3 h-3 text-white/50" />
              <div className="flex flex-wrap gap-1">
                {attendees.slice(0, 3).map((a, i) => (
                  <span
                    key={i}
                    className="px-1.5 py-0.5 rounded bg-white/10 text-white/60"
                  >
                    {a}
                  </span>
                ))}
                {attendees.length > 3 && (
                  <span className="px-1.5 py-0.5 rounded border border-white/20 text-white/40">
                    +{attendees.length - 3}
                  </span>
                )}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
