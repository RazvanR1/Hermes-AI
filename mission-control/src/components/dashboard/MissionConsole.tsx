import { useState } from "react";
import { Sparkles, Send, Brain, ClipboardList, ShieldAlert } from "lucide-react";
import GlassPanel from "../ui/GlassPanel";
import { runMission, type MissionResponse } from "../../api/missions";
import { approveMission } from "../../api/approval";
import { useAgentStore } from "../../context/AgentStore";

const quick = [
  "Actualizează Proxmox",
  "Restart OPNsense",
  "Analyze Docker",
  "Backup Audit",
  "Storage Check",
  "Security Scan",
];

const thinkingSteps = [
  "Reading infrastructure...",
  "Contacting Guardian...",
  "Collecting provider status...",
  "Running reasoning engine...",
  "Building execution plan...",
  "Calculating impact...",
];

export default function MissionConsole() {
  const [mission, setMission] = useState("");
  const [loading, setLoading] = useState(false);
  const [timeline, setTimeline] = useState<string[]>([]);
  const [execution, setExecution] = useState<any>(null);
  const [result, setResult] = useState<MissionResponse | null>(null);
  const { updateAgent, resetAgents } = useAgentStore();

  async function executeMission() {
    if (!mission.trim()) return;

    setLoading(true);
    setResult(null);
    setExecution(null);
    setTimeline([]);
    resetAgents();

    updateAgent("Guardian", {
      status: "running",
      task: "Scanning infrastructure...",
      progress: 15,
      tone: "success",
    });

    for (const step of thinkingSteps) {
      setTimeline((prev) => [...prev, step]);
      await new Promise((r) => setTimeout(r, 350));
    }

    try {
      const res = await runMission(mission);
      setResult(res);

      updateAgent("Planner", {
        status: "ready",
        task: "Plan created with live inventory",
        progress: 100,
        tone: "primary",
      });

      updateAgent("Executor", {
        status: "waiting approval",
        task: "Mission ready",
        progress: 100,
        tone: "warning",
      });
    } finally {
      setLoading(false);
    }
  }

  async function approve() {
    if (!result) return;

    setLoading(true);

    try {
      const res = await approveMission(result.mission, result.plan);
      setExecution(res.executed);

      setTimeline((prev) => [
        ...prev,
        ...res.events.map((e) => `${e.agent}: ${e.status}`),
      ]);

      updateAgent("Executor", {
        status: "running",
        task: "Executing mission...",
        progress: 100,
        tone: "success",
      });
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

      <div className="mt-5 flex flex-wrap gap-3">
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
        <div className="mt-6 rounded-2xl border border-cyan-400/20 bg-slate-950/70 p-6">
          <div className="text-cyan-300 font-bold mb-4">
            Hermes AI is thinking...
          </div>

          <div className="space-y-3">
            {timeline.map((item, index) => (
              <div key={index} className="flex items-center gap-3 text-sm text-slate-300">
                <div className="h-2 w-2 rounded-full bg-cyan-400" />
                {item}
              </div>
            ))}
          </div>
        </div>
      )}

      {execution && (
        <div className="mt-6 rounded-xl border border-cyan-400/20 bg-slate-900/60 p-4">
          <div className="text-lg font-bold mb-4">Execution Report</div>

          <div className="space-y-3">
            {execution.steps.map((s: any) => (
              <div key={s.step} className="rounded-lg bg-slate-950/60 p-3 border border-slate-800">
                <div className="flex justify-between">
                  <div className="font-semibold">{s.title}</div>
                  <div className={s.result?.ok ? "text-emerald-400" : "text-red-400"}>
                    {s.result?.ok ? "OK" : "FAILED"}
                  </div>
                </div>

                <div className="text-xs text-slate-400 mt-1">
                  {s.tool}.{s.action}
                </div>

                <pre className="mt-2 text-xs whitespace-pre-wrap text-slate-300">
                  {s.result?.output}
                </pre>
              </div>
            ))}
          </div>
        </div>
      )}

      {result && (
        <div className="mt-6">
          <div className="grid grid-cols-3 gap-4 mb-6">
            <div className="rounded-xl bg-slate-900/60 p-3">
              <div className="text-xs text-slate-400">Risk</div>
              <div className="text-lg font-bold text-amber-300">
                {result.plan.risk}
              </div>
            </div>

            <div className="rounded-xl bg-slate-900/60 p-3">
              <div className="text-xs text-slate-400">Duration</div>
              <div className="text-lg font-bold">
                {result.plan.estimated_duration} min
              </div>
            </div>

            <div className="rounded-xl bg-slate-900/60 p-3">
              <div className="text-xs text-slate-400">Planner</div>
              <div className="text-lg font-bold text-cyan-300">
                {result.planner}
              </div>
            </div>
          </div>

          <div className="grid grid-cols-1 xl:grid-cols-3 gap-4">
            <div className="rounded-2xl border border-cyan-400/10 bg-slate-950/60 p-5">
              <div className="flex items-center gap-2 text-cyan-300 font-bold mb-3">
                <Brain size={18} /> Inventory Context
              </div>
              <div className="text-sm text-slate-300 leading-6">
                Nodes: {result.plan.inventory.nodes}<br />
                VMs: {result.plan.inventory.vms}<br />
                LXC: {result.plan.inventory.lxc}<br />
                Running: {result.plan.inventory.running}<br />
                Stopped: {result.plan.inventory.stopped}
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
                    <div className="text-xs text-slate-500">{s.action}</div>
                  </div>
                ))}
              </div>
            </div>

            <div className="rounded-2xl border border-amber-400/10 bg-amber-400/5 p-5">
              <div className="flex items-center gap-2 text-amber-300 font-bold mb-3">
                <ShieldAlert size={18} /> Mission Status
              </div>

              <div className="text-sm text-slate-300 leading-6">
                Status: {result.status}
              </div>

              {result.approval_required && (
                <button
                  onClick={approve}
                  className="mt-6 w-full rounded-xl bg-emerald-500 hover:bg-emerald-400 py-3 font-bold text-slate-950 transition"
                >
                  ✅ Approve Mission
                </button>
              )}
            </div>
          </div>
        </div>
      )}
    </GlassPanel>
  );
}
