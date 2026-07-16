import {
  Activity,
  AlertTriangle,
  CheckCircle2,
  MessageSquare,
  Server,
} from "lucide-react";

import { useDashboard } from "../hooks/useDashboard";
import PageContainer from "../components/ui/PageContainer";
import GlassPanel from "../components/ui/GlassPanel";
import ProgressRing from "../components/ui/ProgressRing";
import MissionLog from "../components/dashboard/MissionLog";

export default function HomePage() {
  const { data, loading, error } = useDashboard();

  if (loading) {
    return (
      <PageContainer>
        <div className="text-slate-400">Se încarcă Hermes...</div>
      </PageContainer>
    );
  }

  if (error || !data) {
    return (
      <PageContainer>
        <div className="text-red-400">
          Hermes API nu poate fi contactat.
        </div>
      </PageContainer>
    );
  }

  const hasIncidents = data.health.open_incidents > 0;

  return (
    <PageContainer>
      <div className="space-y-6">
        <header>
          <div className="text-sm uppercase tracking-[0.35em] text-cyan-400">
            Hermes AI OS
          </div>

          <h1 className="mt-2 text-4xl font-black text-white">
            Home
          </h1>

          <p className="mt-2 text-slate-400">
            Starea homelab-ului și lucrurile care necesită atenție.
          </p>
        </header>

        <div className="grid grid-cols-1 gap-6 xl:grid-cols-12">
          <GlassPanel className="p-6 xl:col-span-5">
            <div className="flex items-center justify-between gap-6">
              <div>
                <div className="text-sm text-slate-400">
                  System Health
                </div>

                <div className="mt-2 text-3xl font-bold capitalize text-white">
                  {data.health.status}
                </div>

                <div className="mt-3 flex items-center gap-2 text-sm">
                  {hasIncidents ? (
                    <>
                      <AlertTriangle
                        size={16}
                        className="text-amber-300"
                      />
                      <span className="text-amber-200">
                        {data.health.open_incidents} incident(e) deschis(e)
                      </span>
                    </>
                  ) : (
                    <>
                      <CheckCircle2
                        size={16}
                        className="text-emerald-300"
                      />
                      <span className="text-emerald-200">
                        Nu există incidente active
                      </span>
                    </>
                  )}
                </div>
              </div>

              <ProgressRing value={data.health.score} />
            </div>
          </GlassPanel>

          <GlassPanel className="p-6 xl:col-span-7">
            <div className="mb-5">
              <h2 className="text-xl font-bold text-white">
                Quick Actions
              </h2>

              <p className="mt-1 text-sm text-slate-400">
                Cele mai folosite zone din Hermes.
              </p>
            </div>

            <div className="grid gap-3 sm:grid-cols-3">
              <button
                type="button"
                onClick={() =>
                  window.dispatchEvent(
                    new CustomEvent("hermes:navigate", {
                      detail: "infrastructure",
                    }),
                  )
                }
                className="rounded-2xl border border-cyan-400/15 bg-cyan-400/8 p-4 text-left transition hover:bg-cyan-400/15"
              >
                <Server className="text-cyan-300" size={20} />
                <div className="mt-3 font-semibold text-white">
                  Infrastructure
                </div>
                <div className="mt-1 text-xs text-slate-500">
                  VM-uri, LXC-uri și Proxmox
                </div>
              </button>

              <button
                type="button"
                onClick={() =>
                  window.dispatchEvent(
                    new CustomEvent("hermes:navigate", {
                      detail: "chat",
                    }),
                  )
                }
                className="rounded-2xl border border-violet-400/15 bg-violet-400/8 p-4 text-left transition hover:bg-violet-400/15"
              >
                <MessageSquare
                  className="text-violet-300"
                  size={20}
                />
                <div className="mt-3 font-semibold text-white">
                  AI Chat
                </div>
                <div className="mt-1 text-xs text-slate-500">
                  Vorbește cu Hermes
                </div>
              </button>

              <button
                type="button"
                onClick={() =>
                  window.dispatchEvent(
                    new CustomEvent("hermes:navigate", {
                      detail: "missions",
                    }),
                  )
                }
                className="rounded-2xl border border-emerald-400/15 bg-emerald-400/8 p-4 text-left transition hover:bg-emerald-400/15"
              >
                <Activity
                  className="text-emerald-300"
                  size={20}
                />
                <div className="mt-3 font-semibold text-white">
                  Missions
                </div>
                <div className="mt-1 text-xs text-slate-500">
                  Istoric și aprobări
                </div>
              </button>
            </div>
          </GlassPanel>
        </div>

        <GlassPanel className="p-6">
          <h2 className="text-xl font-bold text-white">
            Active Alerts
          </h2>

          <p className="mt-1 text-sm text-slate-400">
            Probleme și recomandări prioritare.
          </p>

          <div className="mt-5 space-y-3">
            {data.recommendations.length === 0 ? (
              <div className="rounded-2xl border border-emerald-400/15 bg-emerald-400/8 p-4 text-emerald-200">
                Nu există recomandări urgente.
              </div>
            ) : (
              data.recommendations.slice(0, 4).map((item, index) => (
                <div
                  key={`${item.provider}-${index}`}
                  className="rounded-2xl border border-white/8 bg-slate-950/50 p-4"
                >
                  <div className="text-xs font-bold uppercase tracking-[0.16em] text-amber-300">
                    {item.provider}
                  </div>

                  <div className="mt-2 text-sm text-slate-300">
                    {item.recommendation}
                  </div>
                </div>
              ))
            )}
          </div>
        </GlassPanel>

        <GlassPanel className="p-6">
          <h2 className="text-xl font-bold text-white">
            Recent Operations
          </h2>

          <div className="mt-5 space-y-4">
            {data.timeline.slice(0, 5).map((event, index) => (
              <div
                key={`${event.time}-${index}`}
                className="border-l-2 border-cyan-500 pl-4"
              >
                <div className="font-semibold text-white">
                  {event.title}
                </div>

                <div className="mt-1 text-sm text-slate-400">
                  {event.description}
                </div>

                <div className="mt-1 text-xs text-slate-600">
                  {new Date(event.time).toLocaleString()}
                </div>
              </div>
            ))}
          </div>
        </GlassPanel>
      </div>

      <MissionLog />
    </PageContainer>
  );
}
