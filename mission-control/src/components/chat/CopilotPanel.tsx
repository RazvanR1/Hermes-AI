import { useState } from "react";
import { askCopilot } from "../../api/copilot";
import { Bot, User, Send, Sparkles } from "lucide-react";

const suggestions = [
  "Pot face update la Proxmox?",
  "De ce Health Score este 84%?",
  "Rezumă starea homelab-ului",
  "Arată status Docker",
];

export default function CopilotPanel() {
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  const [conversation, setConversation] = useState<any[]>([
    {
      role: "assistant",
      text: "Salut! Sunt Hermes AI. Îți pot explica starea homelab-ului, analiza incidente și recomanda acțiuni.",
    },
  ]);

  async function send(text?: string) {
    const msg = text || message;
    if (!msg.trim()) return;

    setConversation((c) => [...c, { role: "user", text: msg }]);
    setMessage("");
    setLoading(true);

    try {
      const res = await askCopilot(msg);
      setConversation((c) => [
        ...c,
        {
          role: "assistant",
          text: res.answer,
          actions: res.actions || [],
        },
      ]);
    } catch (e) {
      setConversation((c) => [
        ...c,
        {
          role: "assistant",
          text: "Nu am putut contacta Hermes API. Verifică serviciul hermes-api.",
          actions: [],
        },
      ]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="rounded-2xl bg-slate-900 border border-slate-800 p-6">
      <div className="flex items-center gap-3 mb-4">
        <Bot className="text-cyan-400" size={30} />
        <div>
          <div className="font-bold text-xl">Hermes AI Copilot</div>
          <div className="text-slate-500 text-sm">Infrastructure Intelligence</div>
        </div>
      </div>

      <div className="flex flex-wrap gap-2 mb-5">
        {suggestions.map((s) => (
          <button
            key={s}
            onClick={() => send(s)}
            className="rounded-full border border-slate-700 px-3 py-1 text-xs hover:bg-slate-800 transition"
          >
            <Sparkles size={12} className="inline mr-1" />
            {s}
          </button>
        ))}
      </div>

      <div className="space-y-4 max-h-96 overflow-auto mb-4 pr-1">
        {conversation.map((m, i) => (
          <div
            key={i}
            className={
              m.role === "assistant"
                ? "bg-slate-950 border border-slate-800 rounded-xl p-4"
                : "bg-cyan-950/50 border border-cyan-800/40 rounded-xl p-4"
            }
          >
            <div className="flex items-center gap-2 mb-2">
              {m.role === "assistant" ? <Bot size={18} /> : <User size={18} />}
              <div className="font-semibold">{m.role === "assistant" ? "Hermes" : "You"}</div>
            </div>

            <div className="text-sm leading-6 text-slate-200">{m.text}</div>

            {m.actions?.length > 0 && (
              <div className="mt-4 flex flex-wrap gap-2">
                {m.actions.map((a: any, idx: number) => (
                  <button
                    key={idx}
                    className="rounded-lg bg-cyan-600 hover:bg-cyan-500 px-3 py-2 text-sm transition"
                  >
                    {a.title}
                  </button>
                ))}
              </div>
            )}
          </div>
        ))}

        {loading && (
          <div className="bg-slate-950 border border-slate-800 rounded-xl p-4">
            <div className="font-semibold mb-2">🤖 Hermes</div>
            <div className="space-y-2 text-sm text-slate-400">
              <div>✓ Building context...</div>
              <div>✓ Checking Guardian...</div>
              <div>✓ Checking Providers...</div>
              <div>✓ Running Decision Engine...</div>
            </div>
          </div>
        )}
      </div>

      <div className="flex gap-2">
        <input
          className="flex-1 rounded-xl bg-slate-950 border border-slate-700 p-3 outline-none focus:border-cyan-500"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && send()}
          placeholder="Ask Hermes..."
        />

        <button
          onClick={() => send()}
          className="rounded-xl bg-cyan-500 hover:bg-cyan-400 text-slate-950 px-5 transition"
        >
          <Send size={18} />
        </button>
      </div>
    </div>
  );
}
