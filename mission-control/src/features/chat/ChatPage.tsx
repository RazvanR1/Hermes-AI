import { useEffect, useMemo, useRef, useState } from "react";
import { Activity, Bot, ShieldCheck, Sparkles } from "lucide-react";
import { approveMission, rejectMission } from "../../api/approval";
import { getApiErrorMessage } from "../../api/client";
import { runMission, type HermesMission } from "../../api/missions";
import { useAgentStore } from "../../context/AgentStore";
import { useMissionLive } from "../../hooks/useMissionLive";
import ChatHistory from "./components/ChatHistory";
import ChatInput from "./components/ChatInput";
import { useConversation } from "./hooks/useConversation";

const suggestions = [
  "status VM 110",
  "repornește VM 110",
  "pornește VM 110",
  "oprește VM 110",
];

const TERMINAL_STATUSES = new Set([
  "completed",
  "success",
  "succeeded",
  "failed",
  "rejected",
  "blocked",
  "cancelled",
]);

function missionSummary(mission: HermesMission): string {
  const status = mission.status.toLowerCase();
  if (status === "completed") {
    return `Am terminat. Misiunea „${mission.goal}” s-a încheiat cu succes și verificarea a fost înregistrată.`;
  }
  if (status === "failed") {
    return `Execuția pentru „${mission.goal}” a eșuat. Detaliile sunt disponibile în cardul misiunii.`;
  }
  if (status === "rejected") {
    return `Misiunea „${mission.goal}” a fost respinsă și nu a fost executată.`;
  }
  return `Statusul misiunii este acum: ${mission.status}.`;
}

export default function ChatPage() {
  const [input, setInput] = useState("");
  const [planning, setPlanning] = useState(false);
  const [mission, setMission] = useState<HermesMission | null>(null);
  const [busyMissionId, setBusyMissionId] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const previousStatusRef = useRef<string | null>(null);
  const endRef = useRef<HTMLDivElement | null>(null);
  const { updateAgent, resetAgents } = useAgentStore();
  const {
    messages,
    addUserMessage,
    addAssistantMessage,
    addMissionMessage,
    updateMissionMessage,
  } = useConversation();

  const terminal = mission
    ? TERMINAL_STATUSES.has(mission.status.toLowerCase())
    : false;

  const { polling, lastUpdated, error: pollingError } = useMissionLive({
    missionId: mission?.mission_id ?? null,
    enabled: Boolean(mission && !terminal),
    intervalMs: 1500,
    onUpdate: (freshMission) => {
      setMission(freshMission);
      updateMissionMessage(freshMission);

      const currentStatus = freshMission.status.toLowerCase();
      const previousStatus = previousStatusRef.current;
      previousStatusRef.current = currentStatus;

      if (currentStatus !== previousStatus && TERMINAL_STATUSES.has(currentStatus)) {
        addAssistantMessage(missionSummary(freshMission));
      }

      if (["running", "executing"].includes(currentStatus)) {
        updateAgent("Executor", {
          status: "running",
          task: "Mission execution in progress...",
          progress: 75,
          tone: "success",
        });
      }

      if (TERMINAL_STATUSES.has(currentStatus)) {
        setBusyMissionId(null);
        updateAgent("Executor", {
          status: freshMission.status,
          task: `Mission ${freshMission.status}`,
          progress: 100,
          tone: currentStatus === "completed" ? "success" : "warning",
        });
      }
    },
  });

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: "smooth", block: "end" });
  }, [messages, planning, mission?.status]);

  const liveLabel = useMemo(() => {
    if (pollingError) return "Reconectare live...";
    if (polling) return "Live tracking activ";
    if (mission) return `Ultima actualizare ${lastUpdated ? new Date(lastUpdated).toLocaleTimeString() : "acum"}`;
    return "Operator pregătit";
  }, [pollingError, polling, mission, lastUpdated]);

  async function submitMessage(value = input) {
    const message = value.trim();
    if (!message || planning) return;

    setInput("");
    setError(null);
    setPlanning(true);
    setMission(null);
    previousStatusRef.current = null;
    addUserMessage(message);
    addAssistantMessage("Analizez cererea, verific intenția și construiesc planul potrivit...");
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
      const response = await runMission(message);
      setMission(response.mission);
      previousStatusRef.current = response.mission.status.toLowerCase();
      addMissionMessage(
        response.mission,
        response.summary.requires_approval > 0
          ? "Am analizat cererea. Operația necesită aprobarea ta înainte de execuție."
          : "Am analizat cererea. Misiunea este pregătită.",
      );

      updateAgent("Guardian", {
        status: "ready",
        task: `Risk: ${response.summary.overall_risk}`,
        progress: 100,
        tone: response.summary.overall_risk === "SAFE" ? "success" : "warning",
      });
      updateAgent("Planner", {
        status: "ready",
        task: `${response.mission.steps.length} step(s) planned`,
        progress: 100,
        tone: "primary",
      });
      updateAgent("Executor", {
        status: response.summary.requires_approval > 0 ? "waiting approval" : "ready",
        task: response.summary.requires_approval > 0 ? "Mission requires approval" : "Mission ready",
        progress: response.summary.requires_approval > 0 ? 0 : 100,
        tone: response.summary.requires_approval > 0 ? "warning" : "success",
      });
    } catch (requestError) {
      const messageText = getApiErrorMessage(requestError);
      setError(messageText);
      addAssistantMessage(`Nu am putut crea misiunea: ${messageText}`);
      updateAgent("Executor", {
        status: "failed",
        task: messageText,
        progress: 0,
        tone: "warning",
      });
    } finally {
      setPlanning(false);
    }
  }

  async function approveAndRun(targetMission: HermesMission) {
    if (busyMissionId) return;

    const stepIds = targetMission.steps
      .filter((step) => step.requires_confirmation && !step.approved)
      .map((step) => step.id);

    if (stepIds.length === 0) {
      setError("Nu există pași care așteaptă aprobare.");
      return;
    }

    setError(null);
    setBusyMissionId(targetMission.mission_id);
    addAssistantMessage("Aprobarea a fost primită. Pornesc execuția și urmăresc verificarea în timp real.");
    updateAgent("Executor", {
      status: "running",
      task: "Executing approved mission...",
      progress: 65,
      tone: "success",
    });

    try {
      const result = await approveMission(targetMission.mission_id, stepIds);
      if (result.execution.mission) {
        setMission(result.execution.mission);
        updateMissionMessage(result.execution.mission);
      } else if (!result.execution.ok) {
        throw new Error(result.execution.error ?? "Mission execution failed.");
      }
    } catch (requestError) {
      const messageText = getApiErrorMessage(requestError);
      setError(messageText);
      setBusyMissionId(null);
      addAssistantMessage(`Execuția nu a putut porni: ${messageText}`);
    }
  }

  async function reject(targetMission: HermesMission) {
    if (busyMissionId) return;

    const stepIds = targetMission.steps
      .filter((step) => step.requires_confirmation && !step.approved)
      .map((step) => step.id);

    if (stepIds.length === 0) return;

    setBusyMissionId(targetMission.mission_id);
    setError(null);

    try {
      const results = await rejectMission(targetMission.mission_id, stepIds);
      const rejectedMission = [...results]
        .reverse()
        .find((result) => result.mission)?.mission ?? {
        ...targetMission,
        status: "rejected",
        steps: targetMission.steps.map((step) =>
          stepIds.includes(step.id) ? { ...step, status: "rejected" } : step,
        ),
      };

      setMission(rejectedMission);
      updateMissionMessage(rejectedMission);
      addAssistantMessage(`Am respins misiunea „${targetMission.goal}”. Nu a fost executată.`);
    } catch (requestError) {
      const messageText = getApiErrorMessage(requestError);
      setError(messageText);
      addAssistantMessage(`Nu am putut respinge misiunea: ${messageText}`);
    } finally {
      setBusyMissionId(null);
    }
  }

  return (
    <section className="relative overflow-hidden rounded-[32px] border border-white/8 bg-[#07101b]/90 shadow-[0_30px_100px_rgba(0,0,0,0.35)]">
      <div className="pointer-events-none absolute inset-x-0 top-0 h-48 bg-[radial-gradient(circle_at_top,rgba(34,211,238,0.12),transparent_65%)]" />

      <header className="relative flex flex-col gap-5 border-b border-white/8 px-6 py-6 sm:flex-row sm:items-center sm:justify-between lg:px-8">
        <div className="flex items-center gap-4">
          <div className="flex h-12 w-12 items-center justify-center rounded-2xl border border-cyan-300/15 bg-cyan-300/10 text-cyan-300 shadow-[0_0_35px_rgba(34,211,238,0.10)]">
            <Bot size={23} />
          </div>
          <div>
            <div className="text-[11px] font-semibold uppercase tracking-[0.3em] text-cyan-300/80">Hermes AI</div>
            <h2 className="mt-1 text-2xl font-bold tracking-tight text-white">Infrastructure conversation</h2>
            <p className="mt-1 text-sm text-slate-500">Întreabă, aprobă și urmărește execuția în același loc.</p>
          </div>
        </div>

        <div className="flex flex-wrap items-center gap-2 text-xs">
          <span className="inline-flex items-center gap-2 rounded-full border border-emerald-400/15 bg-emerald-400/8 px-3 py-1.5 text-emerald-300">
            <ShieldCheck size={14} /> Approval protected
          </span>
          <span className="inline-flex items-center gap-2 rounded-full border border-cyan-400/15 bg-cyan-400/8 px-3 py-1.5 text-cyan-300">
            <Activity size={14} /> {liveLabel}
          </span>
        </div>
      </header>

      <div className="relative mx-auto max-w-5xl px-5 py-6 sm:px-7 lg:px-10">
        {messages.length === 0 ? (
          <div className="pb-7 pt-2 text-center">
            <div className="mx-auto mb-4 flex h-14 w-14 items-center justify-center rounded-2xl border border-violet-400/15 bg-violet-400/8 text-violet-300">
              <Sparkles size={25} />
            </div>
            <h3 className="text-3xl font-bold tracking-tight text-white">Bună, Mircea.</h3>
            <p className="mx-auto mt-3 max-w-xl text-sm leading-6 text-slate-500">
              Spune-mi ce vrei să verific sau să execut. Operațiile riscante rămân blocate până la aprobarea ta.
            </p>
            <div className="mx-auto mt-6 grid max-w-2xl gap-3 sm:grid-cols-2">
              {suggestions.map((suggestion) => (
                <button
                  key={suggestion}
                  type="button"
                  onClick={() => void submitMessage(suggestion)}
                  className="rounded-2xl border border-white/8 bg-white/[0.025] px-4 py-3 text-left text-sm text-slate-300 transition hover:border-cyan-300/20 hover:bg-cyan-300/5 hover:text-white"
                >
                  {suggestion}
                </button>
              ))}
            </div>
          </div>
        ) : null}

        <ChatHistory
          messages={messages}
          busyMissionId={busyMissionId}
          onApprove={(target) => void approveAndRun(target)}
          onReject={(target) => void reject(target)}
        />

        {error ? (
          <div className="mt-5 rounded-2xl border border-red-400/20 bg-red-400/8 px-4 py-3 text-sm text-red-200">
            {error}
          </div>
        ) : null}

        <div ref={endRef} />
        <ChatInput
          value={input}
          busy={planning}
          onChange={setInput}
          onSubmit={() => void submitMessage()}
        />
      </div>
    </section>
  );
}
