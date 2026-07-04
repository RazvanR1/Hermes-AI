import { useState } from "react";
import { Sparkles, Send, Brain, ClipboardList, ShieldAlert } from "lucide-react";
import GlassPanel from "../ui/GlassPanel";
import { askCopilot, type ExecuteResponse } from "../../api/copilot";

const quick = [
  "Actualizează Proxmox",
  "Restart OPNsense",
  "Analyze Docker",
  "Backup Audit",
  "Storage Check",
  "Security Scan",
];

export default function MissionConsole() {
  const [mission, setMission] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<ExecuteResponse | null>(null);

  async function executeMission() {
    if (!mission.trim()) return;

    setLoading(true);
    setResult(null);

    try {
      const res = await askCopilot(mission, "dashboard");
      setResult(res);
    } finally {
      setLoading(false);
    }
  }

  return (
    <GlassPanel className="p-6">
      <div className="flex items-center gap-3 mb-6">
        <div className="rounded-xl bg-cyan-500/15 p-3">
          <Sparkles className="text-cyan-300" size={22} />
        </div>

        <div>
          <h2 className="text-2xl font-black text-white">Mission Console</h2>
          <p className="text-slate-400 text-sm">
            Tell Hermes what you want to accomplish.
          </p>
        </div>
      </div>

      <textarea
        value={mission}
        onChange={(e) => setMission(e.target.value)}
        placeholder="Example: Update Proxmox after checking backups..."
        className="w-full h-32 rounded-2xl bg-slate-950/60 border border-cyan-400/10 p-5 outline-none resize-none text-white focus:border-cyan-400/40"
      />

      <div className="mt-5">
        <div className="text-xs uppercase tracking-[0.3em] text-slate-500 mb-3">
          Quick Missions
        </div>

        <div className="flex flex-wrap gap-3">
          {quick.map((q) => (
            <button
              key={q}
              onClick={() => setMission(q)}
              className="rounded-full border border-cyan-400/15 bg-cyan-400/5 hover:bg-cyan-400/10 px-4 py-2 text-sm text-cyan-300 transition"
            >
              {q}
            </button>
          ))}
        </div>
      </div>

      <div className="mt-6 flex justify-end">
        <button
          onClick={executeMission}
          disabled={loading}
          className="flex items-center gap-2 rounded-xl bg-cyan-500 hover:bg-cyan-400 disabled:opacity-50 px-6 py-3 font-bold text-slate-950 transition"
        >
          <Send size={18} />
          {loading ? "Executing..." : "Execute Mission"}
        </button>
      </div>

      {loading && (
        <div className="mt-6 rounded-2xl border border-cyan-400/10 bg-slate-950/60 p-5 text-sm text-slate-300 animate-pulse">
          ✓ Building context<br />
          ✓ Running reasoning engine<br />
          ✓ Building execution plan<br />
          ✓ Preparing mission report
        </div>
      )}

      {result && (
        <div className="mt-6 grid grid-cols-1 xl:grid-cols-3 gap-4">
          <div className="rounded-2xl border border-cyan-400/10 bg-slate-950/60 p-5">
            <div className="flex items-center gap-2 text-cyan-300 font-bold mb-3">
              <Brain size={18} /> Reasoning
            </div>
            <div className="text-sm text-slate-300 leading-6">
              {result.reasoning.explanation}
            </div>
            <div className="mt-4 text-xs text-slate-500">
              Score {result.reasoning.score}% → estimated {result.reasoning.estimated_score}%
            </div>
          </div>

          <div className="rounded-2xl border border-cyan-400/10 bg-slate-950/60 p-5">
            <div className="flex items-center gap-2 text-cyan-300 font-bold mb-3">
              <ClipboardList size={18} /> Execution Plan
            </div>
            <div className="space-y-2">
              {result.plan.steps.map((s) => (
                <div key={s.step} className="text-sm text-slate-300">
                  <span className="text-cyan-400">{s.step}.</span> {s.title}
                </div>
              ))}
            </div>
            <div className="mt-4 text-xs text-slate-500">
              ETA {result.plan.estimated_duration} min
            </div>
          </div>

          <div className="rounded-2xl border border-amber-400/10 bg-amber-400/5 p-5">
            <div className="flex items-center gap-2 text-amber-300 font-bold mb-3">
              <ShieldAlert size={18} /> Mission Status
            </div>
            <div className="text-sm text-slate-300 leading-6">
              {result.answer}
            </div>

            {result.actions.length > 0 && (
              <div className="mt-4 flex flex-wrap gap-2">
                {result.actions.map((a) => (
                  <button
                    key={a.action}
                    className="rounded-xl border border-amber-400/20 bg-amber-400/10 px-3 py-2 text-xs text-amber-200"
                  >
                    {a.title}
                  </button>
                ))}
              </div>
            )}
          </div>
        </div>
      )}
    </GlassPanel>
  );
}
