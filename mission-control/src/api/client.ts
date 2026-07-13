import axios from "axios";

const apiBaseUrl =
  import.meta.env.VITE_HERMES_API_URL ??
  "http://192.168.1.202:8088/api/v1";

export const api = axios.create({
  baseURL: apiBaseUrl,
  timeout: 180_000,
  headers: {
    "Content-Type": "application/json",
  },
});

export function getApiErrorMessage(error: unknown): string {
  if (axios.isAxiosError(error)) {
    const detail = error.response?.data?.detail;
    const message = error.response?.data?.message;
    const apiError = error.response?.data?.error;

    if (typeof detail === "string") return detail;
    if (typeof message === "string") return message;
    if (typeof apiError === "string") return apiError;
    if (error.code === "ECONNABORTED") return "Hermes API request timed out.";
    return error.message;
  }

  return error instanceof Error ? error.message : "Unknown Hermes API error.";
}
