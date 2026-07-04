import { api } from "./client";

export interface ExecuteResponse {
  answer: string;
  intent: string;
  reasoning: {
    score: number;
    estimated_score: number;
    explanation: string;
    reasons: string[];
    next_actions: string[];
  };
  plan: {
    task: string;
    estimated_duration: number;
    steps: {
      step: number;
      title: string;
      status: string;
      action: string;
    }[];
  };
  actions: any[];
  history: any[];
}

export async function askCopilot(
  message: string,
  sessionId: string = "dashboard"
): Promise<ExecuteResponse> {

  const res = await api.post(
    "/copilot/execute",
    {
      session_id: sessionId,
      message
    }
  );

  return res.data.data;

}
