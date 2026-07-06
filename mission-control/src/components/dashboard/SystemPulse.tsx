import { Activity, Bot, Server, Shield } from "lucide-react";
import GlassPanel from "../ui/GlassPanel";
import { useHealth } from "../../hooks/useHealth";

export default function SystemPulse() {
  const health = useHealth();

  const score = health?.score ?? 0;
  const incidents = health?.incidents ?? 0;
  const running = health?.summary.running ?? 0;
  const total =
    (health?.summary.running ?? 0) +
    (health?.summary.stopped ?? 0);

  const color =
    health?.status === "healthy"
      ? "text-emerald-400"
      : health?.status === "warning"
      ? "text-amber-400"
      : "text-red-400";

  return (
    <GlassPanel className="p-6">
      <div className="flex items-center justify-between">
        <div>
          <div className="text-xs uppercase tracking-[0.3em] text-cyan-400">
            Hermes Core
          </div>

          <div className={`text-4xl font-black mt-2 ${color}`}>
            {score}%
          </div>

          <div className="text-slate-400 mt-2">
            {health?.status ?? "loading"}
          </div>
        </div>

        <Activity className={color} size={54} />
      </div>

      <div className="grid grid-cols-2 gap-4 mt-8">

        <div className="rounded-xl bg-slate-900/60 p-4">
          <Bot className="mb-2 text-cyan-300"/>
          <div className="text-2xl font-bold">{running}</div>
          <div className="text-xs text-slate-400">
            Running
          </div>
        </div>

        <div className="rounded-xl bg-slate-900/60 p-4">
          <Shield className="mb-2 text-amber-300"/>
          <div className="text-2xl font-bold">{incidents}</div>
          <div className="text-xs text-slate-400">
            Incidents
          </div>
        </div>

        <div className="rounded-xl bg-slate-900/60 p-4">
          <Server className="mb-2 text-violet-300"/>
          <div className="text-2xl font-bold">{total}</div>
          <div className="text-xs text-slate-400">
            Services
          </div>
        </div>

        <div className="rounded-xl bg-slate-900/60 p-4">
          <Activity className="mb-2 text-emerald-300"/>
          <div className="text-2xl font-bold">
            {health?.summary.nodes ?? 0}
          </div>
          <div className="text-xs text-slate-400">
            Nodes
          </div>
        </div>

      </div>
    </GlassPanel>
  );
}
