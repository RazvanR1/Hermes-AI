export default function BackgroundFX() {
  return (
    <div className="fixed inset-0 -z-10 overflow-hidden bg-[#050b14]">
      <div className="absolute -top-40 left-1/4 h-96 w-96 rounded-full bg-cyan-500/20 blur-[120px]" />
      <div className="absolute top-1/3 right-0 h-96 w-96 rounded-full bg-purple-500/10 blur-[120px]" />
      <div className="absolute bottom-0 left-1/3 h-96 w-96 rounded-full bg-emerald-500/10 blur-[140px]" />
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_top,rgba(34,211,238,0.08),transparent_35%),linear-gradient(rgba(255,255,255,0.025)_1px,transparent_1px),linear-gradient(90deg,rgba(255,255,255,0.025)_1px,transparent_1px)] bg-[size:100%_100%,48px_48px,48px_48px]" />
    </div>
  );
}
