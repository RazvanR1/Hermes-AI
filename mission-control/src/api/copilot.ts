import { api } from "./client";

export async function askCopilot(message: string) {
  const res = await api.post("/copilot/chat", { message });
  return res.data.data;
}
