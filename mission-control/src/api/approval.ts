import { api } from "./client";
import type { HermesMission } from "./missions";

export interface ApprovalResult {
  ok: boolean;
  mission?: HermesMission;
  error?: string;
  mission_id?: string;
  step_id?: string;
}

export interface ExecutionResult {
  ok: boolean;
  mission?: HermesMission;
  error?: string;
  mission_id?: string;
}

export interface ApproveAndExecuteResult {
  approvals: ApprovalResult[];
  execution: ExecutionResult;
}

export async function approveStep(
  missionId: string,
  stepId: string,
): Promise<ApprovalResult> {
  const response = await api.post<ApprovalResult>("/approval/v8/approve", {
    mission_id: missionId,
    step_id: stepId,
  });

  return response.data;
}

export async function rejectStep(
  missionId: string,
  stepId: string,
  reason = "Rejected from Hermes Console",
): Promise<ApprovalResult> {
  const response = await api.post<ApprovalResult>("/approval/v8/reject", {
    mission_id: missionId,
    step_id: stepId,
    reason,
  });

  return response.data;
}

export async function executeApprovedMission(
  missionId: string,
): Promise<ExecutionResult> {
  const response = await api.post<ExecutionResult>(
    `/approval/v8/${encodeURIComponent(missionId)}/run-approved`,
  );

  return response.data;
}

export async function approveMission(
  missionId: string,
  stepIds: string[],
): Promise<ApproveAndExecuteResult> {
  const approvals: ApprovalResult[] = [];

  for (const stepId of stepIds) {
    const result = await approveStep(missionId, stepId);
    approvals.push(result);

    if (!result.ok) {
      throw new Error(result.error ?? `Could not approve step ${stepId}.`);
    }
  }

  const execution = await executeApprovedMission(missionId);
  return { approvals, execution };
}

export async function rejectMission(
  missionId: string,
  stepIds: string[],
): Promise<ApprovalResult[]> {
  const rejections: ApprovalResult[] = [];

  for (const stepId of stepIds) {
    rejections.push(await rejectStep(missionId, stepId));
  }

  return rejections;
}
