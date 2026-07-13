import { useMemo, useState } from "react";
import {
  AlertCircle,
  Ban,
  CheckCircle2,
  ClipboardList,
  Clock3,
  Play,
  Send,
  ShieldAlert,
  Sparkles,
  TerminalSquare,
  XCircle,
} from "lucide-react";
import GlassPanel from "../ui/GlassPanel";
import {
  runMission,
  type HermesMission,
  type MissionLogEntry,
  type MissionStep,
  type OperatorResponse,
} from "../../api/missions";
import { approveMission, rejectMission } from "../../api/approval";
import { getApiErrorMessage } from "../../api/client";
import { useAgentStore } from "../../context/AgentStore";
import { useMissionLive } from "../../hooks/useMissionLive";
import { ChatHistory, useConversation } from "../../features/chat";

const quick = [
  "status VM 110",
  "repornește VM 110",
  "pornește VM 110",
  "oprește VM 110",
];

const planningTimeline = [
  "Request received by Hermes Operator",
  "Intent and skill detected",
  "Risk evaluated",
  "Execution plan created",
];

function riskClass(risk: string): string {
  if (risk === "SAFE") return "text-emerald-300";
  if (risk === "BLOCKED") return "text-red-300";
  return "text-amber-300";
}

function statusClass(status: string): string {
  if (["completed", "success", "succeeded"].includes(status)) {
    return "text-emerald-300";
  }
  if (["failed", "rejected", "blocked"].includes(status)) {
    return "text-red-300";
  }
  if (["running", "executing"].includes(status)) return "text-cyan-300";
  return "text-amber-300";
}

function resultOk(step: MissionStep): boolean | null {
  if (!step.result || typeof step.result !== "object") return null;
  const result = step.result as Record<string, unknown>;
  return typeof result.ok === "boolean" ? result.ok : null;
}

function formatJson(value: unknown): string {
  if (value === undefined || value === null) return "";
  try {
    return JSON.stringify(value, null, 2);
  } catch {
    return String(value);
  }
}

const terminalMissionStatuses = new Set([
  "completed",
  "success",
  "succeeded",
  "failed",
  "rejected",
  "blocked",
  "cancelled",
]);

export default function MissionConsole() {
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);
  const [phase, setPhase] = useState<"idle" | "planning" | "approval" | "execution">("idle");
  const [timeline, setTimeline] = useState<string[]>([]);
  const [response, setResponse] = useState<OperatorResponse | null>(null);
  const [mission, setMission] = useState<HermesMission | null>(null);
  const [error, setError] = useState<string | null>(null);
  const { updateAgent, resetAgents } = useAgentStore();

  const {
    messages: conversationMessages,
    addUserMessage,
    addAssistantMessage,
    addMissionMessage,
    updateMissionMessage,
  } = useConversation();

  const missionIsTerminal = mission
    ? terminalMissionStatuses.has(mission.status.toLowerCase())
    : false;

  const {
    polling: missionPolling,
    lastUpdated: missionLastUpdated,
    error: missionPollingError,
  } = useMissionLive({
    missionId: mission?.mission_id ?? null,
    enabled: Boolean(mission && !missionIsTerminal),
    intervalMs: 1500,
    onUpdate: (freshMission) => {
      setMission(freshMission);
      updateMissionMessage(freshMission);

      const freshStatus = freshMission.status.toLowerCase();

      if (freshStatus === "running" || freshStatus === "executing") {
        setPhase("execution");

        updateAgent("Executor", {
          status: "running",
          task: "Mission execution in progress...",
          progress: 75,
          tone: "success",
        });
      }

      if (terminalMissionStatuses.has(freshStatus)) {
        setPhase("execution");

        updateAgent("Executor", {
          status: freshMission.status,
          task: `Mission ${freshMission.status}`,
          progress: 100,
          tone: freshStatus === "completed" ? "success" : "warning",
        });
      }
    },
  });

  const approvalSteps = useMemo(
    () =>
      mission?.steps.filter(
        (step) => step.requires_confirmation && !step.approved,
      ) ?? [],
    [mission],
  );

  const missionLogs: MissionLogEntry[] = mission?.logs ?? [];

  async function createMission() {
    const trimmedMessage = message.trim();
    if (!trimmedMessage || loading) return;

    addUserMessage(trimmedMessage);
    addAssistantMessage("Analizez cererea și construiesc planul de execuție...");

    setLoading(true);
    setPhase("planning");
    setResponse(null);
    setMission(null);
    setError(null);
    setTimeline(planningTimeline);
    resetAgents();

    updateAgent("Guardian", {
      status: "running",
      task: "Evaluating mission risk...",
      progress: 50,
      tone: "success",
    });

    updateAgent("Planner", {
      status: "running",
      task: "Building v8 mission plan...",
      progress: 55,
      tone: "primary",
    });

    try {
      const result = await runMission(trimmedMessage);
      setResponse(result);
      setMission(result.mission);
      addMissionMessage(
        result.mission,
        result.summary.requires_approval > 0
          ? "Am analizat cererea. Misiunea necesită aprobarea ta înainte de execuție."
          : "Am analizat cererea. Misiunea este sigură și poate fi executată.",
      );
      setTimeline((current) => [
        ...current,
        `Mission created: ${result.mission.mission_id}`,
        `Status: ${result.mission.status}`,
      ]);

      updateAgent("Guardian", {
        status: "ready",
        task: `Risk: ${result.summary.overall_risk}`,
        progress: 100,
        tone: result.summary.overall_risk === "SAFE" ? "success" : "warning",
      });

      updateAgent("Planner", {
        status: "ready",
        task: `${result.mission.steps.length} step(s) planned`,
        progress: 100,
        tone: "primary",
      });

      const needsApproval = result.summary.requires_approval > 0;
      setPhase(needsApproval ? "approval" : "execution");

      updateAgent("Executor", {
        status: needsApproval ? "waiting approval" : "ready",
        task: needsApproval ? "Mission requires approval" : "Mission is safe",
        progress: needsApproval ? 0 : 100,
        tone: needsApproval ? "warning" : "success",
      });
    } catch (requestError) {
      const messageText = getApiErrorMessage(requestError);
      setError(messageText);
      setTimeline((current) => [...current, `Error: ${messageText}`]);
      updateAgent("Executor", {
        status: "failed",
        task: messageText,
        progress: 0,
        tone: "warning",
      });
    } finally {
      setLoading(false);
    }
  }

  async function approveAndRun() {
    if (!mission || loading) return;

    const stepIds = approvalSteps.map((step) => step.id);
    if (stepIds.length === 0) {
      setError("No pending approval step was found for this mission.");
      return;
    }

    setLoading(true);
    setPhase("execution");
    setError(null);
    setTimeline((current) => [
      ...current,
      "Approval granted from Hermes Console",
      "Execution pipeline started",
    ]);

    updateAgent("Executor", {
      status: "running",
      task: "Executing approved mission...",
      progress: 65,
      tone: "success",
    });

    try {
      const result = await approveMission(mission.mission_id, stepIds);
      const executedMission = result.execution.mission;

      if (executedMission) {
        setMission(executedMission);
        setTimeline((current) => [
          ...current,
          `Execution finished: ${executedMission.status}`,
        ]);
      } else if (!result.execution.ok) {
        throw new Error(result.execution.error ?? "Mission execution failed.");
      }

      updateAgent("Executor", {
        status: executedMission?.status ?? "finished",
        task: `Mission ${executedMission?.status ?? "finished"}`,
        progress: 100,
        tone: executedMission?.status === "completed" ? "success" : "warning",
      });
    } catch (requestError) {
      const messageText = getApiErrorMessage(requestError);
      setError(messageText);
      setTimeline((current) => [...current, `Execution error: ${messageText}`]);
      updateAgent("Executor", {
        status: "failed",
        task: messageText,
        progress: 100,
        tone: "warning",
      });
    } finally {
      setLoading(false);
    }
  }

  async function rejectPendingMission() {
    if (!mission || loading) return;

    const stepIds = approvalSteps.map((step) => step.id);
    if (stepIds.length === 0) return;

    setLoading(true);
    setError(null);

    try {
      const results = await rejectMission(mission.mission_id, stepIds);
      const rejectedMission = [...results]
        .reverse()
        .find((result) => result.mission)?.mission;

      setMission(
        rejectedMission ?? {
          ...mission,
          status: "rejected",
          steps: mission.steps.map((step) =>
            stepIds.includes(step.id) ? { ...step, status: "rejected" } : step,
          ),
        },
      );
      setTimeline((current) => [...current, "Mission rejected from Hermes Console"]);
      updateAgent("Executor", {
        status: "rejected",
        task: "Mission rejected",
        progress: 100,
        tone: "warning",
      });
    } catch (requestError) {
      setError(getApiErrorMessage(requestError));
    } finally {
      setLoading(false);
    }
  }

  return (
    <GlassPanel className="p-6">
      <div className="mb-6 flex items-center gap-3">
        <div className="rounded-xl bg-cyan-500/15 p-3">
          <Sparkles className="text-cyan-300" size={22} />
        </div>
        <div>
          <h2 className="text-2xl font-black text-white">Hermes Mission Console</h2>
          <p className="text-sm text-slate-400">
            Create, approve and execute a real Hermes v8 mission.
          </p>
        </div>
      </div>

      <ChatHistory messages={conversationMessages} />

      <textarea
        value={message}
        onChange={(event) => setMessage(event.target.value)}
        onKeyDown={(event) => {
          if (event.key === "Enter" && (event.ctrlKey || event.metaKey)) {
            event.preventDefault();
            void createMission();
          }
        }}
        placeholder="Exemplu: repornește VM 110"
        className="h-32 w-full resize-none rounded-2xl border border-cyan-400/10 bg-slate-950/60 p-5 text-white outline-none focus:border-cyan-400/40"
      />

      <div className="mt-5 flex flex-wrap gap-3">
        {quick.map((item) => (
          <button
            key={item}
            type="button"
            onClick={() => setMessage(item)}
            className="rounded-full border border-cyan-400/15 bg-cyan-400/5 px-4 py-2 text-sm text-cyan-300 transition hover:bg-cyan-400/10"
          >
            {item}
          </button>
        ))}
      </div>

      <div className="mt-6 flex justify-end">
        <button
          type="button"
          onClick={() => void createMission()}
          disabled={loading || !message.trim()}
          className="flex items-center gap-2 rounded-xl bg-cyan-500 px-6 py-3 font-bold text-slate-950 transition hover:bg-cyan-400 disabled:cursor-not-allowed disabled:opacity-50"
        >
          <Send size={18} />
          {loading && phase === "planning" ? "Planning..." : "Create Mission"}
        </button>
      </div>

      {mission && (
        <div className="mt-4 flex flex-wrap items-center gap-3 text-xs">
          <span
            className={`inline-flex items-center gap-2 rounded-full border px-3 py-1.5 ${
              missionPolling
                ? "border-cyan-400/20 bg-cyan-400/10 text-cyan-300"
                : "border-slate-700 bg-slate-900/60 text-slate-400"
            }`}
          >
            <span
              className={`h-2 w-2 rounded-full ${
                missionPolling ? "animate-pulse bg-cyan-400" : "bg-slate-500"
              }`}
            />
            {missionPolling ? "Live mission tracking" : "Mission tracking stopped"}
          </span>

          {missionLastUpdated && (
            <span className="text-slate-500">
              Updated: {new Date(missionLastUpdated).toLocaleTimeString()}
            </span>
          )}

          {missionPollingError && (
            <span className="text-amber-300">
              Live refresh retrying...
            </span>
          )}
        </div>
      )}

      {error && (
        <div className="mt-6 flex items-start gap-3 rounded-2xl border border-red-400/20 bg-red-500/10 p-4 text-red-200">
          <AlertCircle className="mt-0.5 shrink-0" size={20} />
          <span className="text-sm">{error}</span>
        </div>
      )}

      {response && mission && (
        <div className="mt-7 space-y-5">
          <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
            <div className="rounded-xl bg-slate-900/60 p-4">
              <div className="text-xs text-slate-400">Mission ID</div>
              <div className="mt-1 break-all font-mono text-xs text-cyan-300">
                {mission.mission_id}
              </div>
            </div>
            <div className="rounded-xl bg-slate-900/60 p-4">
              <div className="text-xs text-slate-400">Risk</div>
              <div className={`mt-1 text-lg font-bold ${riskClass(mission.evaluation.overall_risk)}`}>
                {mission.evaluation.overall_risk}
              </div>
            </div>
            <div className="rounded-xl bg-slate-900/60 p-4">
              <div className="text-xs text-slate-400">Status</div>
              <div className={`mt-1 text-lg font-bold ${statusClass(mission.status)}`}>
                {mission.status}
              </div>
            </div>
            <div className="rounded-xl bg-slate-900/60 p-4">
              <div className="text-xs text-slate-400">Skill</div>
              <div className="mt-1 text-lg font-bold text-violet-300">
                {mission.intent.skill}
              </div>
            </div>
          </div>

          <div className="grid gap-4 xl:grid-cols-3">
            <div className="rounded-2xl border border-cyan-400/10 bg-slate-950/60 p-5 xl:col-span-2">
              <div className="mb-4 flex items-center gap-2 font-bold text-cyan-300">
                <ClipboardList size={18} /> Execution Plan
              </div>
              <div className="space-y-3">
                {mission.steps.map((step, index) => {
                  const ok = resultOk(step);
                  return (
                    <div
                      key={step.id}
                      className="rounded-xl border border-slate-800 bg-slate-900/55 p-4"
                    >
                      <div className="flex flex-wrap items-start justify-between gap-3">
                        <div>
                          <div className="font-semibold text-white">
                            <span className="mr-2 text-cyan-400">{index + 1}.</span>
                            {step.title}
                          </div>
                          <div className="mt-1 font-mono text-xs text-slate-500">
                            {step.action}
                          </div>
                        </div>
                        <div className="flex items-center gap-2 text-xs">
                          <span className={riskClass(step.risk)}>{step.risk}</span>
                          <span className={statusClass(step.status)}>{step.status}</span>
                          {ok === true && <CheckCircle2 className="text-emerald-400" size={17} />}
                          {ok === false && <XCircle className="text-red-400" size={17} />}
                        </div>
                      </div>

                      {Object.keys(step.params ?? {}).length > 0 && (
                        <pre className="mt-3 overflow-auto rounded-lg bg-slate-950/70 p-3 text-xs text-slate-400">
                          {formatJson(step.params)}
                        </pre>
                      )}

                      {step.result !== undefined && (
                        <details className="mt-3">
                          <summary className="cursor-pointer text-xs text-cyan-300">
                            Execution details
                          </summary>
                          <pre className="mt-2 max-h-80 overflow-auto rounded-lg bg-slate-950/70 p-3 text-xs text-slate-300">
                            {formatJson(step.result)}
                          </pre>
                        </details>
                      )}
                    </div>
                  );
                })}
              </div>
            </div>

            <div className="rounded-2xl border border-amber-400/10 bg-amber-400/5 p-5">
              <div className="mb-3 flex items-center gap-2 font-bold text-amber-300">
                <ShieldAlert size={18} /> Mission Control
              </div>
              <div className="space-y-2 text-sm text-slate-300">
                <div>{mission.goal}</div>
                <div className="text-xs text-slate-500">{mission.intent.reason}</div>
                <div className="pt-2">
                  Pending approvals: <strong>{approvalSteps.length}</strong>
                </div>
              </div>

              {approvalSteps.length > 0 && mission.status !== "rejected" && (
                <div className="mt-6 space-y-3">
                  <button
                    type="button"
                    onClick={() => void approveAndRun()}
                    disabled={loading}
                    className="flex w-full items-center justify-center gap-2 rounded-xl bg-emerald-500 py-3 font-bold text-slate-950 transition hover:bg-emerald-400 disabled:opacity-50"
                  >
                    <Play size={18} />
                    {loading && phase === "execution" ? "Executing..." : "Approve & Execute"}
                  </button>
                  <button
                    type="button"
                    onClick={() => void rejectPendingMission()}
                    disabled={loading}
                    className="flex w-full items-center justify-center gap-2 rounded-xl border border-red-400/25 bg-red-500/10 py-3 font-bold text-red-200 transition hover:bg-red-500/20 disabled:opacity-50"
                  >
                    <Ban size={18} /> Reject Mission
                  </button>
                </div>
              )}
            </div>
          </div>

          <div className="grid gap-4 xl:grid-cols-2">
            <div className="rounded-2xl border border-cyan-400/10 bg-slate-950/60 p-5">
              <div className="mb-4 flex items-center gap-2 font-bold text-cyan-300">
                <Clock3 size={18} /> Console Timeline
              </div>
              <div className="space-y-3">
                {timeline.map((item, index) => (
                  <div key={`${item}-${index}`} className="flex items-start gap-3 text-sm text-slate-300">
                    <div className="mt-1.5 h-2 w-2 shrink-0 rounded-full bg-cyan-400" />
                    <span>{item}</span>
                  </div>
                ))}
              </div>
            </div>

            <div className="rounded-2xl border border-violet-400/10 bg-slate-950/60 p-5">
              <div className="mb-4 flex items-center gap-2 font-bold text-violet-300">
                <TerminalSquare size={18} /> Mission Logs
              </div>
              {missionLogs.length === 0 ? (
                <div className="text-sm text-slate-500">No execution logs yet.</div>
              ) : (
                <div className="max-h-80 space-y-3 overflow-auto pr-2">
                  {missionLogs.map((entry, index) => (
                    <div key={`${entry.time}-${index}`} className="border-l border-violet-400/30 pl-3">
                      <div className="text-xs text-slate-500">{entry.time}</div>
                      <div className="text-sm text-slate-300">{entry.message}</div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </GlassPanel>
  );
}
