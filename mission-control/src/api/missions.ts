import { api } from "./client";

export interface PlanStep {
  step: number;
  title: string;
  action: string;
}

export interface MissionPlan {
  ok: boolean;
  goal: string;
  inventory: {
    nodes: number;
    vms: number;
    lxc: number;
    running: number;
    stopped: number;
  };
  estimated_duration: number;
  risk: string;
  steps: PlanStep[];
}

export interface MissionResponse {
  mission: string;
  planner: string;
  approval_required: boolean;
  status: string;
  plan: MissionPlan;
}

export async function runMission(mission: string): Promise<MissionResponse> {
  const res = await api.post("/missions/run", {
    mission,
    session_id: "dashboard",
  });

  return res.data.data;
}
