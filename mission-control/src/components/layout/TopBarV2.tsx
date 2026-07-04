import { Search, Sparkles } from "lucide-react";

export default function TopBarV2() {
  return (
    <header className="sticky top-0 z-10 flex h-20 items-center justify-between border-b border-cyan-400/10 bg-[#050b14]/70 px-8 backdrop-blur-2xl">
      <div>
        <div className="text-sm text-slate-400">Good evening, Mircea</div>
        <div className="text-lg font-bold text-white">Artificial Infrastructure Intelligence</div>
      </div>

      <div className="hidden w-[520px] items-center gap-3 rounded-2xl border border-cyan-400/10 bg-white/[0.03] px-4 py-3 text-slate-400 xl:flex">
        <Search size={18} />
        <span className="text-sm">Search or run command...</span>
        <span className="ml-auto rounded-lg border border-white/10 px-2 py-1 text-xs">Ctrl K</span>
      </div>

      <button className="flex items-center gap-2 rounded-2xl border border-cyan-400/20 bg-cyan-400/10 px-4 py-3 text-sm font-bold text-cyan-200">
        <Sparkles size={16} />
        Ask Hermes
      </button>
    </header>
  );
}
