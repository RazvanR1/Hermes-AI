import KpiCard from "../components/cards/KpiCard";
import TaskTable from "../components/tasks/TaskTable";
import CopilotPanel from "../components/chat/CopilotPanel";
import { useDashboard } from "../hooks/useDashboard";

function ProviderGrid({ providers }: any) {
  return (
    <div className="grid grid-cols-1 lg:grid-cols-5 gap-4">
      {providers.map((p: any) => {
        const warn = p.status === "warning";

        return (
          <div
            key={p.name}
            className="rounded-2xl bg-slate-900 border border-slate-800 p-5"
          >
            <div className="text-sm text-slate-400">{p.name}</div>

            <div
              className={
                warn
                  ? "text-yellow-400 text-xl font-bold mt-2"
                  : "text-green-400 text-xl font-bold mt-2"
              }
            >
              ● {p.primary}
            </div>

            <div className="text-slate-500 text-sm mt-2">
              {p.secondary}
            </div>
          </div>
        );
      })}
    </div>
  );
}

export default function Dashboard() {

  const { data, loading, error } = useDashboard();

  if (loading) {
    return (
      <div className="text-slate-400 text-xl">
        Loading Mission Control...
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-red-400 text-xl">
        Failed to load Dashboard
      </div>
    );
  }

  if (!data) return null;

  return (
    <div className="space-y-6">

      <div>
        <h1 className="text-4xl font-bold">Dashboard</h1>

        <p className="text-slate-400 mt-2">
          Generated at {new Date(data.generated_at).toLocaleString()}
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">

        <KpiCard
          title="Health Score"
          value={`${data.health.score}%`}
          subtitle={data.health.status}
          tone={data.health.status === "healthy" ? "good" : "warn"}
        />

        <KpiCard
          title="Incidents"
          value={data.health.open_incidents}
          subtitle="open incidents"
          tone={data.health.open_incidents > 0 ? "warn" : "good"}
        />

        <KpiCard
          title="Tasks"
          value={data.tasks.length}
          subtitle="recent tasks"
        />

        <KpiCard
          title="Providers"
          value={data.providers.length}
          subtitle="connected systems"
        />

      </div>

      <ProviderGrid providers={data.providers} />

      <div className="grid grid-cols-1 xl:grid-cols-3 gap-6">

        <div className="xl:col-span-2">
          <TaskTable tasks={data.tasks} />
        </div>

        <div className="space-y-6">

          <div className="rounded-2xl bg-slate-900 border border-slate-800 p-6">

            <h2 className="text-xl font-semibold mb-4">
              AI Recommendations
            </h2>

            <div className="space-y-4">

              {data.recommendations.map((r: any, i: number) => (

                <div
                  key={i}
                  className="rounded-xl bg-slate-950 border border-slate-800 p-4"
                >
                  <div className="text-cyan-400 font-semibold">
                    {r.provider.toUpperCase()}
                  </div>

                  <div className="text-slate-300 text-sm mt-1">
                    {r.recommendation}
                  </div>

                </div>

              ))}

            </div>

          </div>

          <CopilotPanel />

        </div>

      </div>

      <div className="rounded-2xl bg-slate-900 border border-slate-800 p-6">

        <h2 className="text-xl font-semibold mb-4">
          Timeline
        </h2>

        <div className="space-y-3">

          {data.timeline.map((e: any, i: number) => (

            <div
              key={i}
              className="border-l-2 border-cyan-500 pl-4"
            >
              <div className="font-semibold">
                {e.title}
              </div>

              <div className="text-sm text-slate-400">
                {e.description}
              </div>

              <div className="text-xs text-slate-600">
                {new Date(e.time).toLocaleString()}
              </div>

            </div>

          ))}

        </div>

      </div>

    </div>
  );
}
