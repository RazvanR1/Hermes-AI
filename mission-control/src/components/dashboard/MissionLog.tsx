import GlassPanel from "../ui/GlassPanel";
import { useMissionLog } from "../../hooks/useMissionLog";

export default function MissionLog() {
  const events = useMissionLog();

  return (
    <GlassPanel className="p-6">
      <div className="text-cyan-400 uppercase tracking-[0.3em] text-xs">
        Live Mission Log
      </div>

      <h2 className="text-2xl font-black mt-2 mb-6">
        Executor Activity
      </h2>

      <div className="space-y-3 max-h-[420px] overflow-auto">
        {events.length === 0 && (
          <div className="text-slate-500">
            No mission activity.
          </div>
        )}

        {events
          .slice()
          .reverse()
          .map((e, i) => (
            <div
              key={i}
              className="rounded-xl border border-slate-800 bg-slate-950/60 p-3"
            >
              <div className="flex justify-between">
                <span className="font-semibold text-cyan-300">
                  {e.agent}
                </span>

                <span className="text-xs text-slate-500">
                  {e.time}
                </span>
              </div>

              <div className="text-sm mt-2 text-slate-300">
                {e.message}
              </div>

              <div className="text-xs mt-2 text-emerald-400">
                {e.status}
              </div>
            </div>
          ))}
      </div>
    </GlassPanel>
  );
}
