import PageContainer from "../components/ui/PageContainer";
import MissionLog from "../components/dashboard/MissionLog";

export default function MissionsPage() {
  return (
    <PageContainer>
      <header className="mb-6">
        <div className="text-sm uppercase tracking-[0.35em] text-cyan-400">
          Operations
        </div>

        <h1 className="mt-2 text-4xl font-black text-white">
          Missions
        </h1>

        <p className="mt-2 text-slate-400">
          Misiuni planificate, aprobări și execuții recente.
        </p>
      </header>

      <MissionLog />
    </PageContainer>
  );
}
