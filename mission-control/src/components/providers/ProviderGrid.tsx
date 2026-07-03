const providers = [
  { name: "Docker", status: "Healthy", meta: "26 containers", tone: "good" },
  { name: "Proxmox", status: "Online", meta: "VM/LXC active", tone: "good" },
  { name: "TrueNAS", status: "Online", meta: "Storage available", tone: "good" },
  { name: "OPNsense", status: "Reboot pending", meta: "12 updates", tone: "warn" },
  { name: "Home Assistant", status: "Online", meta: "Connected", tone: "good" },
];

export default function ProviderGrid() {
  return (
    <div className="grid grid-cols-1 lg:grid-cols-5 gap-4">
      {providers.map((p) => (
        <div key={p.name} className="rounded-2xl bg-slate-900 border border-slate-800 p-5">
          <div className="text-sm text-slate-400">{p.name}</div>
          <div className={p.tone === "warn" ? "text-yellow-400 text-xl font-bold mt-2" : "text-green-400 text-xl font-bold mt-2"}>
            ● {p.status}
          </div>
          <div className="text-slate-500 text-sm mt-2">{p.meta}</div>
        </div>
      ))}
    </div>
  );
}
