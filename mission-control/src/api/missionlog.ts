import { api } from "./client";

export interface MissionEvent {
  time: string;
  agent: string;
  status: string;
  message: string;
}

export async function getMissionLog(): Promise<MissionEvent[]> {
  const res = await api.get("/missionlog");
  return res.data.data;
}
