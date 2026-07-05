import { api } from "./client";

export interface Agent {
  name: string;
  role: string;
  status: string;
  task: string;
  progress: number;
  objects: number;
  cpu: number;
  memory: number;
  last_action: string;
  tone: string;
}

export async function getAgents(): Promise<Agent[]> {
  const res = await api.get("/agents");
  return res.data.data.agents;
}
