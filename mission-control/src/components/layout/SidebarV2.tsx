import {
  Activity,
  Bot,
  Brain,
  ClipboardList,
  Gauge,
  Map,
  RadioTower,
  ScrollText,
  Settings,
  ShieldAlert,
} from "lucide-react";

const items = [
  { label: "Mission Control", icon: Gauge, active: true },
  { label: "AI Agents", icon: Bot },
  { label: "Missions", icon: ClipboardList },
  { label: "Incidents", icon: ShieldAlert },
  { label: "Infrastructure", icon: Map },
  { label: "Knowledge", icon: Brain },
  { label: "Analytics", icon: Activity },
  { label: "Audit Log", icon: ScrollText },
  { label: "Settings", icon: Settings },
];

export default function SidebarV2() {
  return (
    <aside className="fixed left-0 top-0 z-20 h-screen w-72 border-r border-cyan-400/10 bg-slate-950/60 backdrop-blur-2xl p-5">
      <div className="mb-8 rounded-[28px] border border-cyan-400/10 bg-cyan-400/5 p-5 shadow-[0_0_35px_rgba(34,211,238,0.12)]">
        <div className="text-3xl font-black tracking-widest text-white">HERMES</div>
        <div className="mt-1 text-xs uppercase tracking-[0.35em] text-cyan-300">
          AI OS
        </div>
      </div>

      <nav className="space-y-2">
        {items.map((item) => {
          const Icon = item.icon;

          return (
            <button
              key={item.label}
              className={
                "group flex w-full items-center gap-3 rounded-2xl px-4 py-3 text-left text-sm transition " +
                (item.active
                  ? "border border-cyan-400/20 bg-cyan-400/10 text-cyan-200 shadow-[0_0_25px_rgba(34,211,238,0.10)]"
                  : "text-slate-400 hover:bg-white/5 hover:text-white")
              }
            >
              <Icon size={18} />
              <span>{item.label}</span>
            </button>
          );
        })}
      </nav>

      <div className="absolute bottom-5 left-5 right-5 rounded-[24px] border border-emerald-400/10 bg-emerald-400/5 p-4">
        <div className="flex items-center gap-2 text-emerald-300">
          <RadioTower size={16} />
          <span className="text-sm font-bold">System Online</span>
        </div>
        <div className="mt-2 text-xs text-slate-400">v1.0 Alpha · 7 AI Agents</div>
      </div>
    </aside>
  );
}
