import { useEffect, useMemo, useState } from "react";
import {
  Box,
  Boxes,
  Cpu,
  HardDrive,
  MemoryStick,
  RefreshCw,
  Server,
  Square,
} from "lucide-react";

import { api, getApiErrorMessage } from "../api/client";
import { useDashboard } from "../hooks/useDashboard";

import PageContainer from "../components/ui/PageContainer";
import ProgressRing from "../components/ui/ProgressRing";
import GlassPanel from "../components/ui/GlassPanel";
import AIWorkforce from "../components/dashboard/AIWorkforce";
import { ChatPage } from "../features/chat";
import SystemPulse from "../components/dashboard/SystemPulse";
import HeroStats from "../components/dashboard/HeroStats";
import InfrastructureMap from "../components/infrastructure/InfrastructureMap";
import ProviderGrid from "../components/providers/ProviderGrid";
import MissionLog from "../components/dashboard/MissionLog";

type GuestStatus = "running" | "stopped" | string;

interface ProxmoxGuest {
  vmid: number;
  name?: string;
  status: GuestStatus;
  cpu?: number;
  mem?: number;
  maxmem?: number;
  uptime?: number;
  cpus?: number;
  maxdisk?: number;
  disk?: number;
  type?: string;
}

interface ProxmoxNode {
  name: string;
  vms: ProxmoxGuest[];
  lxc: ProxmoxGuest[];
}

interface InventorySummary {
  nodes: number;
  vms: number;
  lxc: number;
  running: number;
  stopped: number;
}

interface InventoryPayload {
  ok: boolean;
  inventory: {
    nodes: ProxmoxNode[];
    summary: InventorySummary;
  };
}

interface InventoryResponse {
  ok: boolean;
  data: InventoryPayload;
  timestamp?: string;
  errors?: string[];
}

function formatBytes(value?: number): string {
  if (!value || value <= 0) {
    return "0 B";
  }

  const units = ["B", "KB", "MB", "GB", "TB"];
  const exponent = Math.min(
    Math.floor(Math.log(value) / Math.log(1024)),
    units.length - 1,
  );

  const amount = value / 1024 ** exponent;

  return `${amount.toFixed(exponent >= 3 ? 1 : 0)} ${units[exponent]}`;
}

function formatPercent(value?: number): string {
  if (value === undefined || Number.isNaN(value)) {
    return "0%";
  }

  return `${(value * 100).toFixed(1)}%`;
}

function formatUptime(seconds?: number): string {
  if (!seconds || seconds <= 0) {
    return "Oprit";
  }

  const days = Math.floor(seconds / 86400);
  const hours = Math.floor((seconds % 86400) / 3600);
  const minutes = Math.floor((seconds % 3600) / 60);

  if (days > 0) {
    return `${days}z ${hours}h`;
  }

  if (hours > 0) {
    return `${hours}h ${minutes}m`;
  }

  return `${minutes}m`;
}

function usagePercent(used?: number, total?: number): number {
  if (!used || !total || total <= 0) {
    return 0;
  }

  return Math.min(100, Math.max(0, (used / total) * 100));
}

function StatusPill({ status }: { status: GuestStatus }) {
  const running = status === "running";

  return (
    <span
      className={[
        "inline-flex items-center gap-2 rounded-full border px-3 py-1 text-xs font-semibold",
        running
          ? "border-emerald-400/20 bg-emerald-400/10 text-emerald-300"
          : "border-rose-400/20 bg-rose-400/10 text-rose-300",
      ].join(" ")}
    >
      <span
        className={[
          "h-2 w-2 rounded-full",
          running ? "bg-emerald-400" : "bg-rose-400",
        ].join(" ")}
      />

      {running ? "Running" : "Stopped"}
    </span>
  );
}

function GuestCard({
  guest,
  guestType,
}: {
  guest: ProxmoxGuest;
  guestType: "VM" | "LXC";
}) {
  const memoryPercent = usagePercent(guest.mem, guest.maxmem);

  return (
    <div className="rounded-2xl border border-white/8 bg-slate-950/45 p-4 transition hover:border-cyan-400/20 hover:bg-slate-950/65">
      <div className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
        <div className="flex min-w-0 items-start gap-3">
          <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl border border-cyan-400/15 bg-cyan-400/10 text-cyan-300">
            {guestType === "VM" ? (
              <Server size={18} />
            ) : (
              <Box size={18} />
            )}
          </div>

          <div className="min-w-0">
            <div className="flex flex-wrap items-center gap-2">
              <span className="text-xs font-semibold uppercase tracking-[0.16em] text-slate-500">
                {guestType} {guest.vmid}
              </span>

              <StatusPill status={guest.status} />
            </div>

            <h3 className="mt-2 truncate text-lg font-bold text-white">
              {guest.name || `${guestType} ${guest.vmid}`}
            </h3>

            <p className="mt-1 text-xs text-slate-500">
              Uptime: {formatUptime(guest.uptime)}
            </p>
          </div>
        </div>

        <div className="grid min-w-[210px] grid-cols-2 gap-3 text-sm">
          <div className="rounded-xl border border-white/6 bg-white/[0.025] p-3">
            <div className="flex items-center gap-2 text-xs text-slate-500">
              <Cpu size={13} />
              CPU
            </div>

            <div className="mt-1 font-semibold text-slate-200">
              {formatPercent(guest.cpu)}
            </div>
          </div>

          <div className="rounded-xl border border-white/6 bg-white/[0.025] p-3">
            <div className="flex items-center gap-2 text-xs text-slate-500">
              <MemoryStick size={13} />
              RAM
            </div>

            <div className="mt-1 font-semibold text-slate-200">
              {memoryPercent.toFixed(1)}%
            </div>
          </div>
        </div>
      </div>

      <div className="mt-4 h-1.5 overflow-hidden rounded-full bg-slate-800">
        <div
          className="h-full rounded-full bg-cyan-400 transition-all"
          style={{ width: `${memoryPercent}%` }}
        />
      </div>

      <div className="mt-2 flex flex-wrap justify-between gap-2 text-xs text-slate-500">
        <span>
          {formatBytes(guest.mem)} / {formatBytes(guest.maxmem)}
        </span>

        <span>{guest.cpus ?? 0} vCPU</span>
      </div>
    </div>
  );
}

export default function DashboardV2() {
  const { data, loading, error } = useDashboard();

  const [inventory, setInventory] = useState<InventoryResponse | null>(null);
  const [inventoryLoading, setInventoryLoading] = useState(true);
  const [inventoryError, setInventoryError] = useState<string | null>(null);
  const [lastInventoryUpdate, setLastInventoryUpdate] = useState<Date | null>(
    null,
  );

  async function loadInventory(silent = false) {
    if (!silent) {
      setInventoryLoading(true);
    }

    try {
      const response = await api.get<InventoryResponse>("/inventory");

      setInventory(response.data);
      setInventoryError(null);
      setLastInventoryUpdate(new Date());
    } catch (requestError) {
      setInventoryError(getApiErrorMessage(requestError));
    } finally {
      setInventoryLoading(false);
    }
  }

  useEffect(() => {
    void loadInventory();

    const interval = window.setInterval(() => {
      void loadInventory(true);
    }, 10_000);

    return () => {
      window.clearInterval(interval);
    };
  }, []);

  const inventoryData = inventory?.data?.inventory;

  const allVirtualMachines = useMemo(
    () => inventoryData?.nodes.flatMap((node) => node.vms ?? []) ?? [],
    [inventoryData],
  );

  const allContainers = useMemo(
    () => inventoryData?.nodes.flatMap((node) => node.lxc ?? []) ?? [],
    [inventoryData],
  );

  if (loading) {
    return (
      <PageContainer>
        <div className="text-slate-400">Loading Hermes...</div>
      </PageContainer>
    );
  }

  if (error || !data) {
    return (
      <PageContainer>
        <div className="text-red-400">Failed to load Hermes.</div>
      </PageContainer>
    );
  }

  return (
    <PageContainer>
      <div className="space-y-6">
        <div className="grid grid-cols-1 gap-6 xl:grid-cols-[1fr_360px]">
          <div className="flex flex-col justify-end">
            <div className="text-sm uppercase tracking-[0.35em] text-cyan-400">
              Hermes AI OS
            </div>

            <h1 className="mt-2 text-5xl font-black">
              Mission Control
            </h1>

            <p className="mt-2 text-slate-400">
              AI-powered infrastructure operations center
            </p>

            <div className="mt-5 w-fit rounded-full border border-cyan-500/30 bg-cyan-500/10 px-5 py-2 text-cyan-300">
              ● Live · {new Date(data.generated_at).toLocaleTimeString()}
            </div>

            <HeroStats />
          </div>

          <SystemPulse />
        </div>

        <AIWorkforce />

        <GlassPanel className="overflow-hidden p-0">
          <div className="flex flex-col gap-4 border-b border-white/8 px-6 py-5 sm:flex-row sm:items-center sm:justify-between">
            <div>
              <div className="flex items-center gap-3">
                <div className="flex h-11 w-11 items-center justify-center rounded-2xl border border-cyan-400/15 bg-cyan-400/10 text-cyan-300">
                  <Boxes size={21} />
                </div>

                <div>
                  <h2 className="text-2xl font-bold text-white">
                    Infrastructure
                  </h2>

                  <p className="mt-1 text-sm text-slate-500">
                    Inventar Proxmox actualizat automat
                  </p>
                </div>
              </div>
            </div>

            <div className="flex items-center gap-3">
              {lastInventoryUpdate ? (
                <span className="text-xs text-slate-500">
                  Actualizat la{" "}
                  {lastInventoryUpdate.toLocaleTimeString()}
                </span>
              ) : null}

              <button
                type="button"
                onClick={() => void loadInventory()}
                disabled={inventoryLoading}
                className="inline-flex items-center gap-2 rounded-xl border border-cyan-400/15 bg-cyan-400/8 px-4 py-2 text-sm font-semibold text-cyan-300 transition hover:bg-cyan-400/15 disabled:cursor-not-allowed disabled:opacity-50"
              >
                <RefreshCw
                  size={15}
                  className={inventoryLoading ? "animate-spin" : ""}
                />
                Refresh
              </button>
            </div>
          </div>

          <div className="p-6">
            {inventoryError ? (
              <div className="rounded-2xl border border-red-400/20 bg-red-400/8 px-4 py-3 text-sm text-red-200">
                Inventory error: {inventoryError}
              </div>
            ) : null}

            {inventoryLoading && !inventoryData ? (
              <div className="py-12 text-center text-slate-500">
                Se încarcă infrastructura...
              </div>
            ) : null}

            {inventoryData ? (
              <div className="space-y-8">
                <div className="grid grid-cols-2 gap-3 md:grid-cols-5">
                  {[
                    {
                      label: "Nodes",
                      value: inventoryData.summary.nodes,
                      icon: Server,
                    },
                    {
                      label: "VMs",
                      value: inventoryData.summary.vms,
                      icon: Square,
                    },
                    {
                      label: "LXC",
                      value: inventoryData.summary.lxc,
                      icon: Box,
                    },
                    {
                      label: "Running",
                      value: inventoryData.summary.running,
                      icon: Cpu,
                    },
                    {
                      label: "Stopped",
                      value: inventoryData.summary.stopped,
                      icon: HardDrive,
                    },
                  ].map((item) => {
                    const Icon = item.icon;

                    return (
                      <div
                        key={item.label}
                        className="rounded-2xl border border-white/8 bg-white/[0.025] p-4"
                      >
                        <div className="flex items-center gap-2 text-xs uppercase tracking-[0.14em] text-slate-500">
                          <Icon size={14} />
                          {item.label}
                        </div>

                        <div className="mt-2 text-3xl font-bold text-white">
                          {item.value}
                        </div>
                      </div>
                    );
                  })}
                </div>

                <section>
                  <div className="mb-4 flex items-end justify-between gap-4">
                    <div>
                      <h3 className="text-xl font-bold text-white">
                        Virtual Machines
                      </h3>

                      <p className="mt-1 text-sm text-slate-500">
                        {allVirtualMachines.length} mașini virtuale detectate
                      </p>
                    </div>
                  </div>

                  <div className="grid gap-4 xl:grid-cols-2">
                    {allVirtualMachines.map((guest) => (
                      <GuestCard
                        key={`vm-${guest.vmid}`}
                        guest={guest}
                        guestType="VM"
                      />
                    ))}
                  </div>
                </section>

                <section>
                  <div className="mb-4 flex items-end justify-between gap-4">
                    <div>
                      <h3 className="text-xl font-bold text-white">
                        LXC Containers
                      </h3>

                      <p className="mt-1 text-sm text-slate-500">
                        {allContainers.length} containere detectate
                      </p>
                    </div>
                  </div>

                  <div className="grid gap-4 xl:grid-cols-2">
                    {allContainers.map((guest) => (
                      <GuestCard
                        key={`lxc-${guest.vmid}`}
                        guest={guest}
                        guestType="LXC"
                      />
                    ))}
                  </div>
                </section>
              </div>
            ) : null}
          </div>
        </GlassPanel>

        <div className="mt-6">
          <ChatPage />
        </div>

        <InfrastructureMap />

        <div className="grid grid-cols-1 gap-6 xl:grid-cols-12">
          <GlassPanel className="bg-gradient-to-br from-slate-900/70 to-cyan-950/30 p-6 xl:col-span-4">
            <div className="flex items-center justify-between">
              <div>
                <div className="text-sm text-slate-400">
                  Overall Health
                </div>

                <div className="mt-2 text-3xl font-bold capitalize">
                  {data.health.status}
                </div>

                <div className="mt-2 text-sm text-slate-500">
                  {data.health.open_incidents} open incident(s)
                </div>
              </div>

              <ProgressRing value={data.health.score} />
            </div>
          </GlassPanel>

          <GlassPanel className="p-6 xl:col-span-8">
            <div className="mb-5">
              <h2 className="text-xl font-bold">
                Infrastructure Providers
              </h2>

              <p className="text-sm text-slate-400">
                Live infrastructure metrics
              </p>
            </div>

            <ProviderGrid />
          </GlassPanel>
        </div>

        <div className="grid grid-cols-1 gap-6 xl:grid-cols-12">
          <GlassPanel className="p-6 xl:col-span-6">
            <h2 className="mb-1 text-xl font-bold">
              AI Insights
            </h2>

            <p className="mb-5 text-sm text-slate-400">
              Most important recommendations
            </p>

            <div className="space-y-4">
              {data.recommendations.map((recommendation, index) => (
                <div
                  key={index}
                  className="rounded-xl border border-slate-800 bg-slate-950/70 p-4"
                >
                  <div className="font-bold uppercase text-amber-300">
                    {recommendation.provider}
                  </div>

                  <div className="mt-2 text-sm text-slate-300">
                    {recommendation.recommendation}
                  </div>
                </div>
              ))}
            </div>
          </GlassPanel>

          <GlassPanel className="p-6 xl:col-span-6">
            <h2 className="mb-1 text-xl font-bold">
              Timeline
            </h2>

            <p className="mb-5 text-sm text-slate-400">
              Recent AI operations
            </p>

            <div className="space-y-4">
              {data.timeline.map((event, index) => (
                <div
                  key={index}
                  className="border-l-2 border-cyan-500 pl-4"
                >
                  <div className="font-bold">
                    {event.title}
                  </div>

                  <div className="text-sm text-slate-400">
                    {event.description}
                  </div>

                  <div className="mt-1 text-xs text-slate-600">
                    {new Date(event.time).toLocaleString()}
                  </div>
                </div>
              ))}
            </div>
          </GlassPanel>
        </div>
      </div>

      <MissionLog />
    </PageContainer>
  );
}
