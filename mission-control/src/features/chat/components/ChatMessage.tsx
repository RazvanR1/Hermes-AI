import { Bot, CircleUserRound, Info, LoaderCircle } from "lucide-react";
import type { HermesMission } from "../../../api/missions";
import MissionCard from "./MissionCard";
import type { ConversationMessage as ConversationMessageType } from "../types";

interface ChatMessageProps {
  message: ConversationMessageType;
  busyMissionId?: string | null;
  onApprove?: (mission: HermesMission) => void;
  onReject?: (mission: HermesMission) => void;
}

export default function ChatMessage({
  message,
  busyMissionId,
  onApprove,
  onReject,
}: ChatMessageProps) {
  if (message.type === "user") {
    return (
      <div className="flex justify-end">
        <div className="max-w-[86%] rounded-[22px] rounded-br-md border border-cyan-300/15 bg-cyan-300/10 px-4 py-3 sm:max-w-[72%]">
          <div className="mb-1.5 flex items-center justify-end gap-2 text-[11px] font-semibold uppercase tracking-[0.16em] text-cyan-300">
            Tu <CircleUserRound size={14} />
          </div>
          <p className="whitespace-pre-wrap text-sm leading-6 text-slate-100">{message.text}</p>
        </div>
      </div>
    );
  }

  if (message.type === "system") {
    return (
      <div className="flex justify-center">
        <div className="inline-flex items-center gap-2 rounded-full border border-white/8 bg-white/[0.03] px-3 py-1.5 text-xs text-slate-500">
          <Info size={13} /> {message.text}
        </div>
      </div>
    );
  }

  if (message.type === "mission" && message.mission) {
    return (
      <div className="flex justify-start">
        <div className="w-full max-w-3xl">
          {message.text ? (
            <div className="mb-3 flex items-start gap-3">
              <div className="mt-0.5 flex h-8 w-8 shrink-0 items-center justify-center rounded-xl border border-violet-400/15 bg-violet-400/10 text-violet-300">
                <Bot size={16} />
              </div>
              <p className="pt-1 text-sm leading-6 text-slate-300">{message.text}</p>
            </div>
          ) : null}
          <MissionCard
            mission={message.mission}
            busy={busyMissionId === message.mission.mission_id}
            onApprove={onApprove}
            onReject={onReject}
          />
        </div>
      </div>
    );
  }

  const isThinking = message.text?.startsWith("Analizez");

  return (
    <div className="flex justify-start">
      <div className="flex max-w-3xl items-start gap-3">
        <div className="mt-0.5 flex h-8 w-8 shrink-0 items-center justify-center rounded-xl border border-violet-400/15 bg-violet-400/10 text-violet-300">
          {isThinking ? <LoaderCircle className="animate-spin" size={16} /> : <Bot size={16} />}
        </div>
        <div className="rounded-[22px] rounded-bl-md border border-white/8 bg-white/[0.025] px-4 py-3">
          <div className="mb-1.5 text-[11px] font-semibold uppercase tracking-[0.16em] text-violet-300">
            Hermes
          </div>
          <p className="whitespace-pre-wrap text-sm leading-6 text-slate-200">{message.text}</p>
        </div>
      </div>
    </div>
  );
}
