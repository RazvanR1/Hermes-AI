import { useState } from "react";
import { Sparkles, Send } from "lucide-react";
import GlassPanel from "../ui/GlassPanel";

const quick = [
  "Update Proxmox",
  "Restart OPNsense",
  "Analyze Docker",
  "Backup Audit",
  "Storage Check",
  "Security Scan",
];

export default function MissionConsole() {
  const [mission, setMission] = useState("");

  return (
    <GlassPanel className="p-6">
      <div className="flex items-center gap-3 mb-6">
        <div className="rounded-xl bg-cyan-500/15 p-3">
          <Sparkles className="text-cyan-300" size={22} />
        </div>

        <div>
          <h2 className="text-2xl font-black text-white">
            Mission Console
          </h2>

          <p className="text-slate-400 text-sm">
            Tell Hermes what you want to accomplish.
          </p>
        </div>
      </div>

      <textarea
        value={mission}
        onChange={(e) => setMission(e.target.value)}
        placeholder="Example: Update Proxmox after checking backups..."
        className="w-full h-36 rounded-2xl bg-slate-950/60 border border-cyan-400/10 p-5 outline-none resize-none text-white"
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
          className="flex items-center gap-2 rounded-xl bg-cyan-500 hover:bg-cyan-400 px-6 py-3 font-bold text-slate-950 transition"
        >
          <Send size={18} />
          Execute Mission
        </button>
      </div>
    </GlassPanel>
  );
}
