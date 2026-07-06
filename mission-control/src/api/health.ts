import { api } from "./client";

export interface LiveHealth {
  score: number;
  status: string;
  incidents: number;
  summary: {
    nodes: number;
    vms: number;
    lxc: number;
    running: number;
    stopped: number;
  };
}

export async function getHealth(): Promise<LiveHealth> {
  const res = await api.get("/health/live");
  return res.data.data;
}
