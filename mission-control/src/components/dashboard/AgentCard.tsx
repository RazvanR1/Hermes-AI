import { Bot, Cpu, MemoryStick } from "lucide-react";
import type { Agent } from "../../api/agents";

function toneClass(tone: string) {
  if (tone === "success") return "border-emerald-400/20 bg-emerald-400/5 text-emerald-300";
  if (tone === "warning") return "border-amber-400/20 bg-amber-400/5 text-amber-300";
  if (tone === "purple") return "border-purple-400/20 bg-purple-400/5 text-purple-300";
  if (tone === "muted") return "border-slate-600/30 bg-slate-700/10 text-slate-400";
  return "border-cyan-400/20 bg-cyan-400/5 text-cyan-300";
}

export default function AgentCard({ agent }: { agent: Agent }) {
  return (
    <div className={"rounded-2xl border p-4 backdrop-blur-xl transition hover:scale-[1.02] " + toneClass(agent.tone)}>
      <div className="flex items-start justify-between">
        <div className="flex gap-3">
          <div className="rounded-xl bg-white/10 p-2">
            <Bot size={20} />
          </div>
          <div>
            <div className="font-black text-white">{agent.name}</div>
            <div className="text-xs opacity-70">{agent.role}</div>
          </div>
        </div>

        <div className="text-xs uppercase tracking-widest">{agent.status}</div>
      </div>

      <div className="mt-4 text-sm text-slate-300">{agent.task}</div>

      <div className="mt-4 h-2 overflow-hidden rounded-full bg-slate-800">
        <div
          className="h-full rounded-full bg-current shadow-[0_0_18px_currentColor]"
          style={{ width: `${agent.progress}%` }}
        />
      </div>

      <div className="mt-3 flex justify-between text-xs text-slate-400">
        <span>{agent.progress}% complete</span>
        <span>{agent.objects} objects</span>
      </div>

      <div className="mt-4 grid grid-cols-2 gap-3 text-xs">
        <div className="rounded-xl bg-black/20 p-3">
          <div className="flex items-center gap-2 text-slate-400">
            <Cpu size={14} /> CPU
          </div>
          <div className="mt-1 font-bold text-white">{agent.cpu}%</div>
        </div>

        <div className="rounded-xl bg-black/20 p-3">
          <div className="flex items-center gap-2 text-slate-400">
            <MemoryStick size={14} /> RAM
          </div>
          <div className="mt-1 font-bold text-white">{agent.memory} MB</div>
        </div>
      </div>

      <div className="mt-3 text-xs text-slate-500">Last action: {agent.last_action}</div>
    </div>
  );
}
