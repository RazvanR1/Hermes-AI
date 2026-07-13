import { MessageSquareText } from "lucide-react";
import ChatMessage from "./ChatMessage";
import type { ConversationMessage } from "../types";

interface ChatHistoryProps {
  messages: ConversationMessage[];
}

export default function ChatHistory({
  messages,
}: ChatHistoryProps) {
  if (messages.length === 0) {
    return (
      <div className="mb-6 flex min-h-40 flex-col items-center justify-center rounded-2xl border border-dashed border-cyan-400/15 bg-slate-950/35 p-6 text-center">
        <MessageSquareText
          className="mb-3 text-cyan-400/60"
          size={28}
        />

        <div className="font-semibold text-slate-300">
          Începe o conversație cu Hermes
        </div>

        <p className="mt-2 max-w-lg text-sm text-slate-500">
          Scrie o comandă precum „status VM 110” sau
          „repornește VM 110”.
        </p>
      </div>
    );
  }

  return (
    <div className="mb-6 max-h-[620px] space-y-4 overflow-y-auto rounded-2xl border border-cyan-400/10 bg-slate-950/35 p-4">
      {messages.map((message) => (
        <ChatMessage
          key={message.id}
          message={message}
        />
      ))}
    </div>
  );
}
