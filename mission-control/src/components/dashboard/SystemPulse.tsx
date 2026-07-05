import { Cpu, Activity, Bot, Server } from "lucide-react";
import GlassPanel from "../ui/GlassPanel";

export default function SystemPulse() {
  return (
    <GlassPanel className="p-6 overflow-hidden relative">
      <div className="absolute right-6 top-6">
        <div className="relative">
          <div className="h-4 w-4 rounded-full bg-emerald-400 animate-ping absolute"></div>
          <div className="h-4 w-4 rounded-full bg-emerald-400 relative"></div>
        </div>
      </div>

      <div className="text-xs uppercase tracking-[0.35em] text-cyan-400">
        Hermes Core
      </div>

      <h2 className="text-3xl font-black mt-2 text-white">
        ONLINE
      </h2>

      <div className="mt-6 grid grid-cols-2 gap-4">

        <div className="rounded-2xl bg-slate-900/60 p-4 border border-cyan-400/10">
          <div className="flex items-center gap-2 text-slate-400 text-sm">
            <Activity size={16}/>
            Health
          </div>

          <div className="mt-2 text-3xl font-black text-emerald-400">
            84%
          </div>
        </div>

        <div className="rounded-2xl bg-slate-900/60 p-4 border border-cyan-400/10">
          <div className="flex items-center gap-2 text-slate-400 text-sm">
            <Bot size={16}/>
            AI Agents
          </div>

          <div className="mt-2 text-3xl font-black text-cyan-300">
            5
          </div>
        </div>

        <div className="rounded-2xl bg-slate-900/60 p-4 border border-cyan-400/10">
          <div className="flex items-center gap-2 text-slate-400 text-sm">
            <Server size={16}/>
            Services
          </div>

          <div className="mt-2 text-3xl font-black text-white">
            42
          </div>
        </div>

        <div className="rounded-2xl bg-slate-900/60 p-4 border border-cyan-400/10">
          <div className="flex items-center gap-2 text-slate-400 text-sm">
            <Cpu size={16}/>
            Tasks
          </div>

          <div className="mt-2 text-3xl font-black text-amber-300">
            2
          </div>
        </div>

      </div>
    </GlassPanel>
  );
}
