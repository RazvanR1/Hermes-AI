import { useDashboard } from "../hooks/useDashboard";
import PageContainer from "../components/ui/PageContainer";
import ProgressRing from "../components/ui/ProgressRing";
import GlassPanel from "../components/ui/GlassPanel";
import AIWorkforce from "../components/dashboard/AIWorkforce";
import MissionConsole from "../components/dashboard/MissionConsole";
import SystemPulse from "../components/dashboard/SystemPulse";
import HeroStats from "../components/dashboard/HeroStats";
import InfrastructureMap from "../components/infrastructure/InfrastructureMap";
import ProviderGrid from "../components/providers/ProviderGrid";


export default function DashboardV2() {
  const { data, loading, error } = useDashboard();

  if (loading) {
    return (
      <PageContainer>
        <div className="text-slate-400">Loading Hermes...</div>
      </PageContainer>
    );
  }

  if (error || !data) {
    return (
      <PageContainer>
        <div className="text-red-400">Failed to load Hermes.</div>
      </PageContainer>
    );
  }

  return (
    <PageContainer>
      <div className="space-y-6">

        <div className="grid grid-cols-1 xl:grid-cols-[1fr_360px] gap-6">
          <div className="flex flex-col justify-end">
            <div className="text-cyan-400 text-sm uppercase tracking-[0.35em]">
              Hermes AI OS
            </div>

            <h1 className="text-5xl font-black mt-2">
              Mission Control
            </h1>

            <p className="text-slate-400 mt-2">
              AI-powered infrastructure operations center
            </p>

            <div className="mt-5 rounded-full border border-cyan-500/30 bg-cyan-500/10 px-5 py-2 text-cyan-300 w-fit">
              ● Live · {new Date(data.generated_at).toLocaleTimeString()}
            </div>
                    <HeroStats />
        </div>

          <SystemPulse />
        </div>

        <AIWorkforce />

        <div className="mt-6">
          <MissionConsole />
        </div>

        <InfrastructureMap />

<div className="grid grid-cols-1 xl:grid-cols-12 gap-6">
          <GlassPanel className="xl:col-span-4 p-6 bg-gradient-to-br from-slate-900/70 to-cyan-950/30">
            <div className="flex items-center justify-between">
              <div>
                <div className="text-slate-400 text-sm">Overall Health</div>
                <div className="text-3xl font-bold mt-2 capitalize">
                  {data.health.status}
                </div>
                <div className="text-slate-500 text-sm mt-2">
                  {data.health.open_incidents} open incident(s)
                </div>
              </div>

              <ProgressRing value={data.health.score} />
            </div>
          </GlassPanel>

          
<GlassPanel className="xl:col-span-8 p-6">
  <div className="mb-5">
    <h2 className="text-xl font-bold">Infrastructure Providers</h2>
    <p className="text-slate-400 text-sm">
      Live infrastructure metrics
    </p>
  </div>

  <ProviderGrid />

</GlassPanel>

        </div>

        <div className="grid grid-cols-1 xl:grid-cols-12 gap-6">
          <GlassPanel className="xl:col-span-6 p-6">
            <h2 className="text-xl font-bold mb-1">AI Insights</h2>
            <p className="text-slate-400 text-sm mb-5">
              Most important recommendations
            </p>

            <div className="space-y-4">
              {data.recommendations.map((r, i) => (
                <div
                  key={i}
                  className="rounded-xl bg-slate-950/70 border border-slate-800 p-4"
                >
                  <div className="text-amber-300 font-bold uppercase">
                    {r.provider}
                  </div>
                  <div className="text-slate-300 text-sm mt-2">
                    {r.recommendation}
                  </div>
                </div>
              ))}
            </div>
          </GlassPanel>

          <GlassPanel className="xl:col-span-6 p-6">
            <h2 className="text-xl font-bold mb-1">Timeline</h2>
            <p className="text-slate-400 text-sm mb-5">
              Recent AI operations
            </p>

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
          </GlassPanel>
        </div>

      </div>
    </PageContainer>
  );
}
