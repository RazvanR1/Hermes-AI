import { api } from "./client";

export async function askCopilot(
  message: string,
  sessionId: string = "dashboard"
) {
  const res = await api.post("/copilot/chat", {
    session_id: sessionId,
    message,
  });

  return res.data.data;
}
