import { useCallback, useState } from "react";
import type { HermesMission } from "../../../api/missions";
import type {
  ConversationMessage,
  ConversationMessageType,
} from "../types";

function generateMessageId(): string {
  if (
    typeof globalThis.crypto !== "undefined" &&
    typeof globalThis.crypto.randomUUID === "function"
  ) {
    return globalThis.crypto.randomUUID();
  }

  return [
    Date.now().toString(36),
    Math.random().toString(36).slice(2, 10),
  ].join("-");
}

function createMessage(
  type: ConversationMessageType,
  text?: string,
  mission?: HermesMission,
): ConversationMessage {
  return {
    id: generateMessageId(),
    type,
    createdAt: new Date().toISOString(),
    text,
    mission,
  };
}

export function useConversation() {
  const [messages, setMessages] = useState<ConversationMessage[]>([]);

  const addUserMessage = useCallback((text: string) => {
    setMessages((current) => [
      ...current,
      createMessage("user", text),
    ]);
  }, []);

  const addAssistantMessage = useCallback((text: string) => {
    setMessages((current) => [
      ...current,
      createMessage("assistant", text),
    ]);
  }, []);

  const addSystemMessage = useCallback((text: string) => {
    setMessages((current) => [
      ...current,
      createMessage("system", text),
    ]);
  }, []);

  const addMissionMessage = useCallback(
    (mission: HermesMission, text?: string) => {
      setMessages((current) => [
        ...current,
        createMessage("mission", text, mission),
      ]);
    },
    [],
  );

  const updateMissionMessage = useCallback(
    (mission: HermesMission) => {
      setMessages((current) =>
        current.map((message) =>
          message.type === "mission" &&
          message.mission?.mission_id === mission.mission_id
            ? {
                ...message,
                mission,
              }
            : message,
        ),
      );
    },
    [],
  );

  const clearConversation = useCallback(() => {
    setMessages([]);
  }, []);

  return {
    messages,
    addUserMessage,
    addAssistantMessage,
    addSystemMessage,
    addMissionMessage,
    updateMissionMessage,
    clearConversation,
  };
}
