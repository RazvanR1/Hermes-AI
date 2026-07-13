import {
  Ban,
  CheckCircle2,
  Circle,
  LoaderCircle,
  Play,
  ShieldAlert,
  XCircle,
} from "lucide-react";
import type { HermesMission, MissionStep } from "../../../api/missions";

interface MissionCardProps {
  mission: HermesMission;
  busy?: boolean;
  onApprove?: (mission: HermesMission) => void;
  onReject?: (mission: HermesMission) => void;
}

const FINAL_STATUSES = new Set([
  "completed",
  "success",
  "succeeded",
  "failed",
  "rejected",
  "blocked",
  "cancelled",
]);

function normalize(value: string | undefined): string {
  return (value ?? "unknown").toLowerCase();
}

function riskClasses(risk: string): string {
  const normalized = risk.toUpperCase();
  if (normalized === "SAFE") {
    return "border-emerald-400/20 bg-emerald-400/10 text-emerald-300";
  }
  if (normalized === "BLOCKED") {
    return "border-red-400/20 bg-red-400/10 text-red-300";
  }
  return "border-amber-400/20 bg-amber-400/10 text-amber-300";
}

function statusClasses(status: string): string {
  const normalized = normalize(status);
  if (["completed", "success", "succeeded"].includes(normalized)) {
    return "text-emerald-300";
  }
  if (["failed", "rejected", "blocked", "cancelled"].includes(normalized)) {
    return "text-red-300";
  }
  if (["running", "executing", "approved"].includes(normalized)) {
    return "text-cyan-300";
  }
  return "text-amber-300";
}

function stepIcon(step: MissionStep) {
  const status = normalize(step.status);

  if (["completed", "success", "succeeded"].includes(status)) {
    return <CheckCircle2 className="text-emerald-400" size={17} />;
  }

  if (["failed", "rejected", "blocked"].includes(status)) {
    return <XCircle className="text-red-400" size={17} />;
  }

  if (["running", "executing", "approved"].includes(status)) {
    return <LoaderCircle className="animate-spin text-cyan-400" size={17} />;
  }

  return <Circle className="text-slate-600" size={17} />;
}

export default function MissionCard({
  mission,
  busy = false,
  onApprove,
  onReject,
}: MissionCardProps) {
  const pendingSteps = mission.steps.filter(
    (step) => step.requires_confirmation && !step.approved,
  );
  const status = normalize(mission.status);
  const terminal = FINAL_STATUSES.has(status);

  return (
    <article className="overflow-hidden rounded-[24px] border border-white/10 bg-[#0c1320]/95 shadow-[0_18px_70px_rgba(0,0,0,0.35)]">
      <div className="border-b border-white/8 px-5 py-4">
        <div className="flex flex-wrap items-start justify-between gap-4">
          <div>
            <div className="mb-1 text-[11px] font-semibold uppercase tracking-[0.22em] text-cyan-300/80">
              Mission
            </div>
            <h3 className="text-lg font-semibold text-white">{mission.goal}</h3>
            <p className="mt-1 text-sm text-slate-500">{mission.intent.reason}</p>
          </div>

          <div className="flex items-center gap-2">
            <span className={`rounded-full border px-3 py-1 text-xs font-semibold ${riskClasses(mission.evaluation.overall_risk)}`}>
              {mission.evaluation.overall_risk}
            </span>
            <span className={`rounded-full border border-white/10 bg-white/[0.03] px-3 py-1 text-xs font-semibold ${statusClasses(mission.status)}`}>
              {mission.status}
            </span>
          </div>
        </div>
      </div>

      <div className="space-y-3 px-5 py-4">
        {mission.steps.map((step, index) => (
          <div
            key={step.id}
            className="flex items-start gap-3 rounded-2xl border border-white/7 bg-black/20 px-4 py-3"
          >
            <div className="mt-0.5">{stepIcon(step)}</div>
            <div className="min-w-0 flex-1">
              <div className="flex items-start justify-between gap-3">
                <div>
                  <div className="text-sm font-medium text-slate-100">
                    {index + 1}. {step.title}
                  </div>
                  <div className="mt-1 truncate font-mono text-[11px] text-slate-500">
                    {step.action}
                  </div>
                </div>
                <span className={`shrink-0 text-xs font-medium ${statusClasses(step.status)}`}>
                  {step.status}
                </span>
              </div>
            </div>
          </div>
        ))}
      </div>

      {(pendingSteps.length > 0 || terminal) && (
        <div className="border-t border-white/8 bg-black/15 px-5 py-4">
          {pendingSteps.length > 0 && !terminal ? (
            <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
              <div className="flex items-center gap-2 text-sm text-amber-200">
                <ShieldAlert size={17} />
                Confirmarea ta este necesară înainte de execuție.
              </div>
              <div className="flex gap-2">
                <button
                  type="button"
                  disabled={busy}
                  onClick={() => onReject?.(mission)}
                  className="inline-flex items-center gap-2 rounded-xl border border-red-400/20 bg-red-400/8 px-4 py-2.5 text-sm font-semibold text-red-200 transition hover:bg-red-400/15 disabled:cursor-not-allowed disabled:opacity-50"
                >
                  <Ban size={16} /> Respinge
                </button>
                <button
                  type="button"
                  disabled={busy}
                  onClick={() => onApprove?.(mission)}
                  className="inline-flex items-center gap-2 rounded-xl bg-cyan-400 px-4 py-2.5 text-sm font-bold text-slate-950 transition hover:bg-cyan-300 disabled:cursor-not-allowed disabled:opacity-50"
                >
                  {busy ? <LoaderCircle className="animate-spin" size={16} /> : <Play size={16} />}
                  {busy ? "Execut..." : "Aprobă și execută"}
                </button>
              </div>
            </div>
          ) : (
            <div className={`flex items-center gap-2 text-sm font-medium ${statusClasses(mission.status)}`}>
              {status === "completed" ? <CheckCircle2 size={17} /> : null}
              Misiune {mission.status}
            </div>
          )}
        </div>
      )}
    </article>
  );
}
