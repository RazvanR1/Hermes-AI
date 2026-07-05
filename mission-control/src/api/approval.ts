import { api } from "./client";

export interface ApprovalResponse {
  status: string;
  message: string;
  events: {
    agent: string;
    status: string;
  }[];
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
