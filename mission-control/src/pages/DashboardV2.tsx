import { Cpu, Shield, Server, Database, Home, Activity } from "lucide-react";
import { useDashboard } from "../hooks/useDashboard";
import Card from "../components/ui/Card";
import PageContainer from "../components/ui/PageContainer";
import ProgressRing from "../components/ui/ProgressRing";
import StatusBadge from "../components/ui/StatusBadge";
import CopilotPanel from "../components/chat/CopilotPanel";
import AIWorkforce from "../components/dashboard/AIWorkforce";

const agentCards = [
  { name: "Guardian", status: "Scanning", progress: "98%", color: "text-green-400" },
  { name: "Planner", status: "Ready", progress: "100%", color: "text-cyan-400" },
  { name: "Reasoner", status: "Analyzing", progress: "84%", color: "text-purple-400" },
  { name: "Executor", status: "Waiting", progress: "0%", color: "text-amber-400" },
];

function iconFor(name: string) {
  if (name === "Docker") return <Cpu size={22} />;
  if (name === "Proxmox") return <Server size={22} />;
  if (name === "TrueNAS") return <Database size={22} />;
  if (name === "OPNsense") return <Shield size={22} />;
  if (name === "Home Assistant") return <Home size={22} />;
  return <Activity size={22} />;
}

export default function DashboardV2() {
  const { data, loading, error } = useDashboard();

  if (loading) return <PageContainer><div className="text-slate-400">Loading Hermes...</div></PageContainer>;
  if (error || !data) return <PageContainer><div className="text-red-400">Failed to load Hermes.</div></PageContainer>;

  return (
    <PageContainer>
      <div className="space-y-6">
        <div className="flex flex-col xl:flex-row xl:items-end xl:justify-between gap-4">
          <div>
            <div className="text-cyan-400 text-sm uppercase tracking-[0.35em]">Hermes AI OS</div>
            <h1 className="text-5xl font-black mt-2">Mission Control</h1>
            <p className="text-slate-400 mt-2">
              AI-powered infrastructure operations center
            </p>
          </div>

          <div className="rounded-full border border-cyan-500/30 bg-cyan-500/10 px-5 py-2 text-cyan-300">
            ● Live · {new Date(data.generated_at).toLocaleTimeString()}
          </div>
        </div>

        <AIWorkforce />

        <div className="grid grid-cols-1 xl:grid-cols-12 gap-6">
          <Card className="xl:col-span-4 bg-gradient-to-br from-slate-900 to-cyan-950/30">
            <div className="flex items-center justify-between">
              <div>
                <div className="text-slate-400 text-sm">Overall Health</div>
                <div className="text-3xl font-bold mt-2 capitalize">{data.health.status}</div>
                <div className="text-slate-500 text-sm mt-2">
                  {data.health.open_incidents} open incident(s)
                </div>
              </div>
              <ProgressRing value={data.health.score} />
            </div>
          </Card>

          <Card className="xl:col-span-8">
            <div className="flex items-center justify-between mb-5">
              <div>
                <h2 className="text-xl font-bold">Infrastructure</h2>
                <p className="text-slate-400 text-sm">Connected providers</p>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
              {data.providers.map((p) => (
                <div key={p.name} className="rounded-2xl bg-slate-950/70 border border-slate-800 p-4 hover:border-cyan-500/40 transition">
                  <div className="flex items-center justify-between">
                    <div className="text-cyan-300">{iconFor(p.name)}</div>
                    <StatusBadge status={p.status} />
                  </div>
                  <div className="font-bold mt-4">{p.name}</div>
                  <div className="text-2xl font-black mt-1">{p.primary}</div>
                  <div className="text-slate-500 text-sm mt-1">{p.secondary}</div>
                </div>
              ))}
            </div>
          </Card>
        </div>

        <div className="grid grid-cols-1 xl:grid-cols-12 gap-6">
          <Card className="xl:col-span-4">
            <h2 className="text-xl font-bold mb-1">Active AI Agents</h2>
            <p className="text-slate-400 text-sm mb-5">Hermes workforce</p>

            <div className="space-y-4">
              {agentCards.map((a) => (
                <div key={a.name} className="rounded-xl bg-slate-950/70 border border-slate-800 p-4">
                  <div className="flex justify-between">
                    <div className="font-bold">{a.name}</div>
                    <div className={a.color}>{a.progress}</div>
                  </div>
                  <div className="text-slate-400 text-sm mt-1">{a.status}</div>
                  <div className="h-2 rounded-full bg-slate-800 mt-3 overflow-hidden">
                    <div className="h-full bg-cyan-400" style={{ width: a.progress }} />
                  </div>
                </div>
              ))}
            </div>
          </Card>

          <Card className="xl:col-span-4">
            <h2 className="text-xl font-bold mb-1">AI Insights</h2>
            <p className="text-slate-400 text-sm mb-5">Most important recommendations</p>

            <div className="space-y-4">
              {data.recommendations.map((r, i) => (
                <div key={i} className="rounded-xl bg-slate-950/70 border border-slate-800 p-4">
                  <div className="text-amber-300 font-bold">{r.provider}</div>
                  <div className="text-slate-300 text-sm mt-2">{r.recommendation}</div>
                </div>
              ))}
            </div>
          </Card>

          <Card className="xl:col-span-4">
            <h2 className="text-xl font-bold mb-1">Timeline</h2>
            <p className="text-slate-400 text-sm mb-5">Recent AI operations</p>

            <div className="space-y-4">
              {data.timeline.map((e, i) => (
                <div key={i} className="border-l-2 border-cyan-500 pl-4">
                  <div className="font-bold">{e.title}</div>
                  <div className="text-slate-400 text-sm">{e.description}</div>
                  <div className="text-slate-600 text-xs mt-1">
                    {new Date(e.time).toLocaleString()}
                  </div>
                </div>
              ))}
            </div>
          </Card>
        </div>

        <Card>
          <CopilotPanel />
        </Card>
      </div>
    </PageContainer>
  );
}
