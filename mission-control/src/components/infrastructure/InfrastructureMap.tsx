import GlassPanel from "../ui/GlassPanel";
import {
  Globe,
  Shield,
  Server,
  Database,
  Home,
  Container,
  HardDrive
} from "lucide-react";

function Node({
  icon,
  title,
  color = "emerald"
}:{
  icon:React.ReactNode;
  title:string;
  color?:string;
}){

const colors:any={
emerald:"border-emerald-400/40 text-emerald-300 shadow-[0_0_30px_rgba(16,185,129,.25)]",
cyan:"border-cyan-400/40 text-cyan-300 shadow-[0_0_30px_rgba(34,211,238,.25)]",
amber:"border-amber-400/40 text-amber-300 shadow-[0_0_30px_rgba(251,191,36,.25)]",
violet:"border-violet-400/40 text-violet-300 shadow-[0_0_30px_rgba(167,139,250,.25)]"
}

return(

<div className={`relative rounded-2xl border bg-slate-950/70 p-4 ${colors[color]}`}>

<div className="absolute right-3 top-3 h-2 w-2 rounded-full bg-emerald-400 animate-pulse"/>

<div className="flex justify-center mb-3">
{icon}
</div>

<div className="text-center font-bold">
{title}
</div>

</div>

)

}

export default function InfrastructureMap(){

return(

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
Realtime
</div>

</div>

<div className="flex flex-col items-center gap-8">

<Node icon={<Globe size={34}/>} title="Internet" color="cyan"/>

<div className="h-10 w-px bg-cyan-500/40"/>

<Node icon={<Shield size={34}/>} title="OPNsense"/>

<div className="h-10 w-px bg-cyan-500/40"/>

<Node icon={<Server size={34}/>} title="Proxmox" color="violet"/>

<div className="grid grid-cols-4 gap-10 w-full mt-2">

<Node icon={<Container size={30}/>} title="Docker" color="cyan"/>

<Node icon={<Database size={30}/>} title="TrueNAS"/>

<Node icon={<Home size={30}/>} title="Home Assistant" color="amber"/>

<Node icon={<HardDrive size={30}/>} title="Backups"/>

</div>

</div>

</GlassPanel>

)

}
