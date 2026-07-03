import { Home, MessageSquare, ClipboardList, AlertTriangle, Network } from "lucide-react";

const items = [
  { icon: Home, label: "Dashboard" },
  { icon: MessageSquare, label: "Chat" },
  { icon: ClipboardList, label: "Tasks" },
  { icon: AlertTriangle, label: "Incidents" },
  { icon: Network, label: "Knowledge Graph" },
];

export default function Sidebar() {
  return (
    <aside className="w-64 bg-slate-900 border-r border-slate-800 p-6">
      <h1 className="text-2xl font-bold mb-8 text-cyan-400">Hermes</h1>

      <nav className="space-y-2">
        {items.map((item) => {
          const Icon = item.icon;
          return (
            <button
              key={item.label}
              className="w-full flex items-center gap-3 rounded-lg px-3 py-3 text-slate-300 hover:bg-slate-800 hover:text-white transition"
            >
              <Icon size={20} />
              {item.label}
            </button>
          );
        })}
      </nav>
    </aside>
  );
}
