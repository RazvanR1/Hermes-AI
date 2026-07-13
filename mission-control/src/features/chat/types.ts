import type { HermesMission } from "../../api/missions";

export type ConversationMessageType =
  | "user"
  | "assistant"
  | "mission"
  | "system";

export interface ConversationMessage {
  id: string;
  type: ConversationMessageType;
  createdAt: string;
  text?: string;
  mission?: HermesMission;
}
