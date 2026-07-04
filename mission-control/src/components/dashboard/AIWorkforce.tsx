import { useAgents } from "../../hooks/useAgents";
import GlassPanel from "../ui/GlassPanel";
import AgentCard from "./AgentCard";

export default function AIWorkforce() {
  const { agents, loading } = useAgents();

  return (
    <GlassPanel className="p-6">
      <div className="mb-5 flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-black">AI Workforce</h2>
          <p className="text-sm text-slate-400">Live Hermes agents activity</p>
        </div>

        <div className="rounded-full border border-cyan-400/20 bg-cyan-400/10 px-4 py-2 text-xs font-bold text-cyan-300">
          {loading ? "SYNCING" : `${agents.length} AGENTS ONLINE`}
        </div>
      </div>

      <div className="grid grid-cols-1 gap-4 xl:grid-cols-5">
        {agents.map((agent) => (
          <AgentCard key={agent.name} agent={agent} />
        ))}
      </div>
    </GlassPanel>
  );
}
