import ProviderCard from "./ProviderCard";

const providers = [
  {
    name: "Proxmox",
    status: "healthy",
    cpu: 21,
    ram: 9.8,
    ramTotal: 32,
    network: "1.2 Gbps",
    uptime: "31 days",
    lastSync: "2 sec ago",
  },
  {
    name: "Docker",
    status: "healthy",
    cpu: 18,
    ram: 4.2,
    ramTotal: 8,
    network: "420 Mbps",
    uptime: "14 days",
    lastSync: "1 sec ago",
  },
  {
    name: "TrueNAS",
    status: "warning",
    cpu: 12,
    ram: 18,
    ramTotal: 32,
    network: "780 Mbps",
    uptime: "52 days",
    lastSync: "3 sec ago",
  },
  {
    name: "OPNsense",
    status: "healthy",
    cpu: 8,
    ram: 2.1,
    ramTotal: 8,
    network: "980 Mbps",
    uptime: "19 days",
    lastSync: "2 sec ago",
  },
  {
    name: "Home Assistant",
    status: "healthy",
    cpu: 14,
    ram: 3.6,
    ramTotal: 8,
    network: "35 Mbps",
    uptime: "11 days",
    lastSync: "2 sec ago",
  },
];

export default function ProviderGrid() {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
      {providers.map((provider) => (
        <ProviderCard
          key={provider.name}
          {...provider}
        />
      ))}
    </div>
  );
}
