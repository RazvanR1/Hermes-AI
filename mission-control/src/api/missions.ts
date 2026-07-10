import { api } from "./client";

export type MissionRisk = "SAFE" | "CONFIRM" | "BLOCKED" | string;

export interface MissionStep {
  id: string;
  title: string;
  action: string;
  params: Record<string, unknown>;
  risk: MissionRisk;
  status: string;
  requires_confirmation: boolean;
  blocked: boolean;
  approved?: boolean;
  result?: unknown;
  verification?: unknown;
  started_at?: string;
  finished_at?: string;
}

export interface MissionEvaluation {
  overall_risk: MissionRisk;
  safe_count: number;
  confirm_count: number;
  blocked_count: number;
  safe: MissionStep[];
  requires_confirmation: MissionStep[];
  blocked: MissionStep[];
}

export interface MissionLogEntry {
  time: string;
  level: string;
  message: string;
  data?: Record<string, unknown>;
}

export interface HermesMission {
  ok: boolean;
  mission_id: string;
  created_at: string;
  updated_at?: string;
  goal: string;
  status: string;
  intent: {
    intent: string;
    skill: string;
    risk: MissionRisk;
    reason: string;
  };
  evaluation: MissionEvaluation;
  steps: MissionStep[];
  execution: Record<string, unknown>;
  source?: string;
  requested_by?: string;
  logs?: MissionLogEntry[];
}

export interface OperatorResponse {
  ok: boolean;
  message: string;
  source: string;
  user: string;
  intent: HermesMission["intent"];
  mission: HermesMission;
  summary: {
    mission_id: string;
    status: string;
    overall_risk: MissionRisk;
    safe_steps: number;
    requires_approval: number;
  };
}

export async function runMission(message: string): Promise<OperatorResponse> {
  const response = await api.post<OperatorResponse>("/operator/v8/chat", {
    message,
    source: "mission-control",
    user: "mircea",
  });

  return response.data;
}

export async function getMission(
  missionId: string,
): Promise<HermesMission> {
  const response = await api.get<
    HermesMission | { ok: boolean; mission?: HermesMission }
  >(`/mission/v8/${encodeURIComponent(missionId)}`);

  const payload = response.data;

  if ("mission" in payload && payload.mission) {
    return payload.mission;
  }

  return payload as HermesMission;
}
