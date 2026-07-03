import { api } from "./client";

export async function runCopilotAction(action: string, payload: Record<string, unknown> = {}) {
  const res = await api.post("/copilot/action", {
    action,
    payload,
  });

  return res.data.data;
}
