import { useEffect, useState } from "react";
import { getAgents } from "../api/agents";
import type { Agent } from "../api/agents";

export function useAgents() {
  const [agents, setAgents] = useState<Agent[]>([]);
  const [loading, setLoading] = useState(true);

  async function refresh() {
    const data = await getAgents();
    setAgents(data);
    setLoading(false);
  }

  useEffect(() => {
    refresh();
    const timer = setInterval(refresh, 10000);
    return () => clearInterval(timer);
  }, []);

  return { agents, loading };
}
