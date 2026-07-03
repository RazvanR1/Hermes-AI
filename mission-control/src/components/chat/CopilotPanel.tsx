import { useState } from "react";
import { askCopilot } from "../../api/copilot";
import {
  Bot,
  User,
  Send,
  Sparkles
} from "lucide-react";

const suggestions = [
  "Pot face update la Proxmox?",
  "De ce Health Score este 84%?",
  "Rezumă homelab-ul",
  "Arată status Docker",
];

export default function CopilotPanel() {

  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  const [conversation, setConversation] = useState<any[]>([
    {
      role: "assistant",
      text: "Salut! Sunt Hermes AI. Îți pot explica infrastructura și pot recomanda acțiuni."
    }
  ]);

  async function typeAnswer(answer: string, actions: any[]) {

    let current = "";

    setConversation(c => [
      ...c,
      {
        role: "assistant",
        text: "",
        actions: []
      }
    ]);

    for (const ch of answer) {

      current += ch;

      setConversation(c => {

        const copy = [...c];

        copy[copy.length - 1] = {
          role: "assistant",
          text: current,
          actions: []
        };

        return copy;

      });

      await new Promise(r => setTimeout(r, 12));

    }

    setConversation(c => {

      const copy = [...c];

      copy[copy.length - 1] = {
        role: "assistant",
        text: answer,
        actions
      };

      return copy;

    });

  }

  async function send(text?: string) {

    const msg = text || message;

    if (!msg.trim()) return;

    setConversation(c => [
      ...c,
      {
        role: "user",
        text: msg
      }
    ]);

    setMessage("");

    setLoading(true);

    try {

      const res = await askCopilot(
        msg,
        "dashboard"
      );

      await typeAnswer(
        res.answer,
        res.actions || []
      );

    } finally {

      setLoading(false);

    }

  }

  return (

    <div className="rounded-2xl bg-slate-900 border border-slate-800 p-6">

      <div className="flex items-center gap-3 mb-4">

        <Bot
          className="text-cyan-400"
          size={28}
        />

        <div>

          <div className="font-bold text-xl">
            Hermes AI
          </div>

          <div className="text-slate-500 text-sm">
            Infrastructure Copilot
          </div>

        </div>

      </div>

      <div className="flex flex-wrap gap-2 mb-5">

        {suggestions.map(s => (

          <button
            key={s}
            onClick={() => send(s)}
            className="rounded-full border border-slate-700 px-3 py-1 text-xs hover:bg-slate-800 transition"
          >

            <Sparkles
              size={12}
              className="inline mr-1"
            />

            {s}

          </button>

        ))}

      </div>

      <div className="space-y-4 h-96 overflow-auto mb-5 pr-2">

        {conversation.map((m, i) => (

          <div
            key={i}
            className={
              m.role === "assistant"
                ? "bg-slate-950 border border-slate-800 rounded-xl p-4"
                : "bg-cyan-950/50 border border-cyan-700 rounded-xl p-4"
            }
          >

            <div className="flex items-center gap-2 mb-2">

              {m.role === "assistant"
                ? <Bot size={18}/>
                : <User size={18}/>
              }

              <div className="font-semibold">

                {m.role === "assistant"
                  ? "Hermes"
                  : "You"
                }

              </div>

            </div>

            <div className="text-sm leading-7 whitespace-pre-wrap">

              {m.text}

            </div>

            {m.actions?.length > 0 && (

              <div className="mt-4 flex flex-wrap gap-2">

                {m.actions.map((a:any,i:number)=>(

                  <button
                    key={i}
                    className="rounded-lg bg-cyan-600 hover:bg-cyan-500 transition px-3 py-2 text-sm"
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

            <div className="font-semibold mb-3">
              🤖 Hermes
            </div>

            <div className="space-y-2 text-sm text-slate-400 animate-pulse">

              <div>✓ Building Context</div>

              <div>✓ Guardian</div>

              <div>✓ Providers</div>

              <div>✓ Decision Engine</div>

            </div>

          </div>

        )}

      </div>

      <div className="flex gap-2">

        <input
          value={message}
          onChange={e=>setMessage(e.target.value)}
          onKeyDown={e=>e.key==="Enter"&&send()}
          placeholder="Ask Hermes..."
          className="flex-1 rounded-xl bg-slate-950 border border-slate-700 p-3 outline-none focus:border-cyan-500"
        />

        <button
          onClick={()=>send()}
          className="rounded-xl bg-cyan-500 hover:bg-cyan-400 px-5 text-slate-950 transition"
        >

          <Send size={18}/>

        </button>

      </div>

    </div>

  );

}
