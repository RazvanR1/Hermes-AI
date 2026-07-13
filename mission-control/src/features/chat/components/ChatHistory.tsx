import { MessageSquareText } from "lucide-react";
import type { HermesMission } from "../../../api/missions";
import ChatMessage from "./ChatMessage";
import type { ConversationMessage } from "../types";

interface ChatHistoryProps {
  messages: ConversationMessage[];
  busyMissionId?: string | null;
  onApprove?: (mission: HermesMission) => void;
  onReject?: (mission: HermesMission) => void;
}

export default function ChatHistory({
  messages,
  busyMissionId,
  onApprove,
  onReject,
}: ChatHistoryProps) {
  if (messages.length === 0) {
    return (
      <div className="flex min-h-[280px] flex-col items-center justify-center rounded-[28px] border border-dashed border-white/10 bg-white/[0.018] p-8 text-center">
        <div className="mb-4 flex h-12 w-12 items-center justify-center rounded-2xl border border-cyan-300/15 bg-cyan-300/8 text-cyan-300">
          <MessageSquareText size={23} />
        </div>
        <div className="text-base font-semibold text-slate-200">Conversația începe aici</div>
        <p className="mt-2 max-w-md text-sm leading-6 text-slate-500">
          Cere o explicație sau pornește o operație reală: „status VM 110” ori „repornește VM 110”.
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-5 py-2">
      {messages.map((message) => (
        <ChatMessage
          key={message.id}
          message={message}
          busyMissionId={busyMissionId}
          onApprove={onApprove}
          onReject={onReject}
        />
      ))}
    </div>
  );
}
