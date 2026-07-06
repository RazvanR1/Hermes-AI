import {
  Globe,
  Shield,
  Server,
  Database,
  Home,
  Container,
  HardDrive,
  Monitor,
} from "lucide-react";
import GlassPanel from "../ui/GlassPanel";
import { useInventory } from "../../hooks/useInventory";

function NodeCard({
  icon,
  title,
  subtitle,
  status = "running",
}: {
  icon: React.ReactNode;
  title: string;
  subtitle?: string;
  status?: string;
}) {
  const online = status === "running" || status === "online";

  return (
    <div className="relative rounded-2xl border border-cyan-400/20 bg-slate-950/70 p-4 shadow-[0_0_30px_rgba(34,211,238,.12)]">
      <div
        className={
          "absolute right-3 top-3 h-2 w-2 rounded-full animate-pulse " +
          (online ? "bg-emerald-400" : "bg-red-400")
        }
      />

      <div className="flex justify-center mb-3 text-cyan-300">
        {icon}
      </div>

      <div className="text-center font-bold text-white">
        {title}
      </div>

      {subtitle && (
        <div className="text-center text-xs text-slate-500 mt-1">
          {subtitle}
        </div>
      )}
    </div>
  );
}

export default function InfrastructureMap() {
  const inv = useInventory();
  const node = inv?.inventory.nodes?.[0];

  const vms = node?.vms ?? [];
  const lxc = node?.lxc ?? [];

  return (
    <GlassPanel className="p-8">
      <div className="flex items-center justify-between mb-8">
        <div>
          <div className="text-cyan-400 uppercase tracking-[0.3em] text-xs">
            Infrastructure Graph
          </div>

          <h2 className="text-3xl font-black mt-2">
            Live Infrastructure
          </h2>
        </div>

        <div className="rounded-full bg-cyan-500/10 border border-cyan-500/20 px-4 py-2 text-cyan-300 text-sm">
          Inventory API
        </div>
      </div>

      <div className="flex flex-col items-center gap-8">
        <NodeCard icon={<Globe size={34} />} title="Internet" status="online" />

        <div className="h-10 w-px bg-cyan-500/40" />

        <NodeCard icon={<Shield size={34} />} title="OPNsense" status="online" />

        <div className="h-10 w-px bg-cyan-500/40" />

        <NodeCard
          icon={<Server size={34} />}
          title={node?.name ?? "Proxmox"}
          subtitle={`${vms.length} VM · ${lxc.length} LXC`}
          status="online"
        />

        <div className="grid grid-cols-1 md:grid-cols-3 xl:grid-cols-4 gap-5 w-full mt-2">
          {vms.map((vm: any) => (
            <NodeCard
              key={`vm-${vm.vmid}`}
              icon={
                vm.name?.toLowerCase().includes("haos") ? (
                  <Home size={28} />
                ) : vm.name?.toLowerCase().includes("truenas") ? (
                  <Database size={28} />
                ) : (
                  <Monitor size={28} />
                )
              }
              title={vm.name || `VM ${vm.vmid}`}
              subtitle={`VM ${vm.vmid}`}
              status={vm.status}
            />
          ))}

          {lxc.map((ct: any) => (
            <NodeCard
              key={`ct-${ct.vmid}`}
              icon={
                ct.name?.toLowerCase().includes("portainer") ? (
                  <Container size={28} />
                ) : ct.name?.toLowerCase().includes("ollama") ? (
                  <Server size={28} />
                ) : (
                  <HardDrive size={28} />
                )
              }
              title={ct.name || `CT ${ct.vmid}`}
              subtitle={`LXC ${ct.vmid}`}
              status={ct.status}
            />
          ))}
        </div>
      </div>
    </GlassPanel>
  );
}
