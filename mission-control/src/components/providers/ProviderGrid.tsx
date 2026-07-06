import ProviderCard from "./ProviderCard";
import { useInventory } from "../../hooks/useInventory";

export default function ProviderGrid() {
  const inv = useInventory();
  const summary = inv?.inventory.summary;

  const providers = [
    {
      name: "Proxmox",
      status: summary ? "healthy" : "warning",
      cpu: 15,
      ram: 26,
      ramTotal: 32,
      network: "Live",
      uptime: "Online",
      lastSync: "Inventory API",
    },
    {
      name: "Virtual Machines",
      status: "healthy",
      cpu: summary ? Math.round((summary.running / Math.max(summary.vms + summary.lxc, 1)) * 100) : 0,
      ram: summary?.vms ?? 0,
      ramTotal: Math.max(summary?.vms ?? 1, 1),
      network: `${summary?.running ?? "-"} running`,
      uptime: `${summary?.stopped ?? "-"} stopped`,
      lastSync: "Proxmox",
    },
    {
      name: "LXC Containers",
      status: "healthy",
      cpu: summary ? Math.round((summary.lxc / Math.max(summary.vms + summary.lxc, 1)) * 100) : 0,
      ram: summary?.lxc ?? 0,
      ramTotal: Math.max((summary?.vms ?? 0) + (summary?.lxc ?? 1), 1),
      network: `${summary?.lxc ?? "-"} total`,
      uptime: "Live",
      lastSync: "Proxmox",
    },
  ];

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
      {providers.map((provider) => (
        <ProviderCard key={provider.name} {...provider} />
      ))}
    </div>
  );
}
