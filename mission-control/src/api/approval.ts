import { api } from "./client";

export interface ApprovalResponse {
  status: string;
  message: string;
  mission: string;

  events: {
    agent: string;
    status: string;
  }[];

  executed: {
    ok: boolean;
    steps: {
      step: number;
      title: string;
      tool: string;
      action: string;
      result: {
        ok: boolean;
        output?: string;
        error?: string;
      };
    }[];
  };
}

export async function approveMission(
  mission: string,
  approved = true
): Promise<ApprovalResponse> {
  const res = await api.post("/missions/approve", {
    mission,
    approved,
  });

  return res.data.data;
}
