export default function KpiCard({ title, value, subtitle, tone = "default" }: any) {
  const tones: any = {
    default: "border-slate-800",
    good: "border-green-500/30",
    warn: "border-yellow-500/30",
    bad: "border-red-500/30",
  };

  return (
    <div className={`rounded-2xl bg-slate-900 border ${tones[tone]} p-5`}>
      <div className="text-slate-400 text-sm">{title}</div>
      <div className="text-3xl font-bold mt-2">{value}</div>
      <div className="text-slate-500 text-sm mt-2">{subtitle}</div>
    </div>
  );
}
