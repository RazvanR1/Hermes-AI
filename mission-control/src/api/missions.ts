import { api } from "./client";

export interface MissionResponse {
  mode: string;
  mission: string;
  status: string;
  risk: string;
  approval_required: boolean;

  plan: {
    estimated_duration: number;
    steps: {
      step: number;
      title: string;
      status: string;
      action: string;
    }[];
  };

  reasoning: any;

  steps: {
    agent: string;
    status: string;
    message: string;
    confidence: number;
    output?: any;
  }[];

  report: {
    summary: string;
    recommendation: string;
  };
}

export async function runMission(
  mission: string,
  session = "dashboard"
): Promise<MissionResponse> {
  const res = await api.post("/missions/run", {
    mission,
    session_id: session,
  });

  return res.data.data;
}
