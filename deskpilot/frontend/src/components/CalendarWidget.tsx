"use client";

import { useEffect, useState } from "react";
import { Calendar, Loader2, RefreshCw } from "lucide-react";
import { API_URL } from "@/config/api";

interface CalEvent {
  summary: string;
  start: string;
  end?: string;
  location?: string;
}

export function CalendarWidget() {
  const [events, setEvents] = useState<CalEvent[]>([]);
  const [loading, setLoading] = useState(true);

  async function load() {
    setLoading(true);
    try {
      const token = localStorage.getItem("dp_token");
      const res = await fetch(`${API_URL}/calendar/events?days=7`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      if (res.ok) {
        const data = await res.json();
        setEvents(Array.isArray(data) ? data : []);
      }
    } catch {
      setEvents([]);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    load();
  }, []);

  return (
    <div className="rounded-xl border border-white/10 bg-white/5 backdrop-blur-md overflow-hidden">
      <div className="flex items-center justify-between px-4 py-3 border-b border-white/10">
        <div className="flex items-center gap-2">
          <Calendar className="w-4 h-4 text-purple-400" />
          <span className="text-sm font-semibold text-white">Upcoming</span>
        </div>
        <button onClick={load} className="text-white/30 hover:text-white transition-colors">
          <RefreshCw className="w-3.5 h-3.5" />
        </button>
      </div>

      <div className="p-3 space-y-2 max-h-80 overflow-y-auto">
        {loading ? (
          <div className="flex items-center justify-center py-6">
            <Loader2 className="w-4 h-4 animate-spin text-purple-400" />
          </div>
        ) : events.length === 0 ? (
          <p className="text-xs text-white/30 text-center py-4">No events in the next 7 days</p>
        ) : (
          events.map((ev, i) => (
            <div
              key={i}
              className="rounded-lg bg-white/5 border border-white/10 p-2.5 hover:border-purple-400/30 transition-colors"
            >
              <p className="text-xs font-medium text-white line-clamp-1">{ev.summary}</p>
              <p className="text-[10px] text-white/40 mt-0.5">{ev.start}</p>
              {ev.location && (
                <p className="text-[10px] text-white/30 truncate">{ev.location}</p>
              )}
            </div>
          ))
        )}
      </div>
    </div>
  );
}
