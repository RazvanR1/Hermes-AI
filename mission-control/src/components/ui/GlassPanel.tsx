import type { ReactNode } from "react";

export default function GlassPanel({
  children,
  className = "",
}: {
  children: ReactNode;
  className?: string;
}) {
  return (
    <div
      className={
        "rounded-[28px] border border-cyan-400/10 bg-slate-950/45 backdrop-blur-xl shadow-[0_0_0_1px_rgba(34,211,238,0.05),0_20px_60px_rgba(0,0,0,0.45)] " +
        className
      }
    >
      {children}
    </div>
  );
}
