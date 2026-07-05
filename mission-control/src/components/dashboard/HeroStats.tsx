import { Activity, Bot, Shield, Zap } from "lucide-react";
import GlassPanel from "../ui/GlassPanel";

const stats = [
  {
    icon: Activity,
    title: "Health Score",
    value: "84%",
    color: "text-emerald-400",
    glow: "shadow-[0_0_20px_rgba(16,185,129,.35)]",
  },
  {
    icon: Bot,
    title: "AI Agents",
    value: "5",
    color: "text-cyan-300",
    glow: "shadow-[0_0_20px_rgba(34,211,238,.35)]",
  },
  {
    icon: Shield,
    title: "Incidents",
    value: "1",
    color: "text-amber-300",
    glow: "shadow-[0_0_20px_rgba(251,191,36,.35)]",
  },
  {
    icon: Zap,
    title: "Tasks",
    value: "2",
    color: "text-violet-300",
    glow: "shadow-[0_0_20px_rgba(167,139,250,.35)]",
  },
];

export default function HeroStats() {
  return (
    <div className="grid grid-cols-2 xl:grid-cols-4 gap-4 mt-6">
      {stats.map((s) => {
        const Icon = s.icon;

        return (
          <GlassPanel
            key={s.title}
            className={`p-5 transition hover:scale-[1.02] ${s.glow}`}
          >
            <div className="flex items-center justify-between">
              <Icon className={s.color} size={22} />
              <div className="h-2 w-2 rounded-full bg-emerald-400 animate-pulse" />
            </div>

            <div className="text-slate-500 text-sm mt-4">
              {s.title}
            </div>

            <div className={`text-4xl font-black mt-2 ${s.color}`}>
              {s.value}
            </div>
          </GlassPanel>
        );
      })}
    </div>
  );
}
