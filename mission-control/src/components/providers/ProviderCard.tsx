import {
  Cpu,
  MemoryStick,
  Network,
  Clock3,
  CheckCircle2,
  AlertTriangle,
} from "lucide-react";
import GlassPanel from "../ui/GlassPanel";

export interface ProviderCardProps {
  name: string;
  status: string;
  cpu: number;
  ram: number;
  ramTotal: number;
  network: string;
  uptime: string;
  lastSync: string;
}

function StatusIcon(status: string) {
  if (status === "healthy") {
    return <CheckCircle2 size={16} className="text-emerald-400" />;
  }

  return <AlertTriangle size={16} className="text-amber-400" />;
}

export default function ProviderCard(props: ProviderCardProps) {
  const cpuWidth = Math.min(props.cpu, 100);
  const ramPercent = Math.min(
    (props.ram / props.ramTotal) * 100,
    100
  );

  return (
    <GlassPanel className="p-5 hover:scale-[1.02] transition-all">

      <div className="flex justify-between items-center">

        <div>
          <div className="text-xl font-black">
            {props.name}
          </div>

          <div className="flex items-center gap-2 mt-1 text-sm text-slate-400">
            {StatusIcon(props.status)}
            {props.status}
          </div>
        </div>

        <div className="h-3 w-3 rounded-full bg-emerald-400 animate-pulse shadow-[0_0_14px_rgba(16,185,129,.8)]" />

      </div>

      <div className="mt-6 space-y-5">

        <div>

          <div className="flex justify-between text-sm mb-1">

            <div className="flex gap-2 items-center">
              <Cpu size={15}/>
              CPU
            </div>

            <div>{props.cpu}%</div>

          </div>

          <div className="h-2 rounded-full bg-slate-800">

            <div
              className="h-2 rounded-full bg-cyan-400 transition-all duration-700"
              style={{ width: `${cpuWidth}%` }}
            />

          </div>

        </div>

        <div>

          <div className="flex justify-between text-sm mb-1">

            <div className="flex gap-2 items-center">
              <MemoryStick size={15}/>
              Memory
            </div>

            <div>
              {props.ram} / {props.ramTotal} GB
            </div>

          </div>

          <div className="h-2 rounded-full bg-slate-800">

            <div
              className="h-2 rounded-full bg-violet-400 transition-all duration-700"
              style={{ width: `${ramPercent}%` }}
            />

          </div>

        </div>

        <div className="grid grid-cols-2 gap-4 text-sm">

          <div className="rounded-xl bg-slate-900/70 p-3">

            <div className="flex gap-2 items-center text-slate-400">
              <Network size={14}/>
              Network
            </div>

            <div className="mt-2 font-bold">
              {props.network}
            </div>

          </div>

          <div className="rounded-xl bg-slate-900/70 p-3">

            <div className="flex gap-2 items-center text-slate-400">
              <Clock3 size={14}/>
              Uptime
            </div>

            <div className="mt-2 font-bold">
              {props.uptime}
            </div>

          </div>

        </div>

        <div className="text-xs text-slate-500">
          Last Sync • {props.lastSync}
        </div>

      </div>

    </GlassPanel>
  );
}
