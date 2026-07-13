import {
  Bot,
  CheckCircle2,
  CircleUserRound,
  Info,
} from "lucide-react";
import type { ConversationMessage as ConversationMessageType } from "../types";

interface ChatMessageProps {
  message: ConversationMessageType;
}

function statusClass(status: string): string {
  const normalized = status.toLowerCase();

  if (["completed", "success", "succeeded"].includes(normalized)) {
    return "text-emerald-300";
  }

  if (["failed", "rejected", "blocked"].includes(normalized)) {
    return "text-red-300";
  }

  if (["running", "executing"].includes(normalized)) {
    return "text-cyan-300";
  }

  return "text-amber-300";
}

export default function ChatMessage({ message }: ChatMessageProps) {
  if (message.type === "user") {
    return (
      <div className="flex justify-end">
        <div className="max-w-[85%] rounded-2xl rounded-br-md border border-cyan-400/15 bg-cyan-500/10 px-4 py-3">
          <div className="mb-2 flex items-center justify-end gap-2 text-xs font-semibold text-cyan-300">
            Tu
            <CircleUserRound size={15} />
          </div>

          <p className="whitespace-pre-wrap text-sm leading-6 text-slate-100">
            {message.text}
          </p>
        </div>
      </div>
    );
  }

  if (message.type === "system") {
    return (
      <div className="flex justify-center">
        <div className="inline-flex items-center gap-2 rounded-full border border-slate-700 bg-slate-900/70 px-4 py-2 text-xs text-slate-400">
          <Info size={14} />
          {message.text}
        </div>
      </div>
    );
  }

  if (message.type === "mission" && message.mission) {
    const mission = message.mission;

    return (
      <div className="flex justify-start">
        <div className="w-full max-w-[92%] rounded-2xl rounded-bl-md border border-violet-400/15 bg-slate-950/75 p-4">
          <div className="mb-3 flex items-center gap-2 text-sm font-semibold text-violet-300">
            <Bot size={17} />
            Hermes
          </div>

          {message.text && (
            <p className="mb-4 text-sm leading-6 text-slate-300">
              {message.text}
            </p>
          )}

          <div className="grid gap-3 sm:grid-cols-3">
            <div className="rounded-xl bg-slate-900/70 p-3">
              <div className="text-xs text-slate-500">Risc</div>
              <div className="mt-1 font-bold text-amber-300">
                {mission.evaluation.overall_risk}
              </div>
            </div>

            <div className="rounded-xl bg-slate-900/70 p-3">
              <div className="text-xs text-slate-500">Status</div>
              <div className={`mt-1 font-bold ${statusClass(mission.status)}`}>
                {mission.status}
              </div>
            </div>

            <div className="rounded-xl bg-slate-900/70 p-3">
              <div className="text-xs text-slate-500">Skill</div>
              <div className="mt-1 font-bold text-violet-300">
                {mission.intent.skill}
              </div>
            </div>
          </div>

          <div className="mt-4 space-y-2">
            {mission.steps.map((step) => (
              <div
                key={step.id}
                className="flex items-center justify-between gap-3 rounded-lg border border-slate-800 bg-slate-900/55 px-3 py-2"
              >
                <div>
                  <div className="text-sm text-slate-200">
                    {step.title}
                  </div>

                  <div className="font-mono text-xs text-slate-500">
                    {step.action}
                  </div>
                </div>

                <div className="flex items-center gap-2">
                  {step.status === "completed" && (
                    <CheckCircle2
                      className="text-emerald-400"
                      size={16}
                    />
                  )}

                  <span className={`text-xs ${statusClass(step.status)}`}>
                    {step.status}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="flex justify-start">
      <div className="max-w-[85%] rounded-2xl rounded-bl-md border border-violet-400/15 bg-violet-500/5 px-4 py-3">
        <div className="mb-2 flex items-center gap-2 text-xs font-semibold text-violet-300">
          <Bot size={15} />
          Hermes
        </div>

        <p className="whitespace-pre-wrap text-sm leading-6 text-slate-200">
          {message.text}
        </p>
      </div>
    </div>
  );
}
