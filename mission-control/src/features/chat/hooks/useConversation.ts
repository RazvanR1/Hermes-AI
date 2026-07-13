import { useCallback, useMemo, useState } from "react";
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
    Math.random().toString(36).slice(2),
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
  const [isThinking, setThinking] = useState(false);

  const addMessage = useCallback(
    (
      type: ConversationMessageType,
      text?: string,
      mission?: HermesMission,
    ) => {
      setMessages((current) => [
        ...current,
        createMessage(type, text, mission),
      ]);
    },
    [],
  );

  const addUserMessage = useCallback(
    (text: string) => {
      addMessage("user", text);
    },
    [addMessage],
  );

  const addAssistantMessage = useCallback(
    (text: string) => {
      addMessage("assistant", text);
    },
    [addMessage],
  );

  const addSystemMessage = useCallback(
    (text: string) => {
      addMessage("system", text);
    },
    [addMessage],
  );

  const addMissionMessage = useCallback(
    (mission: HermesMission, text?: string) => {
      addMessage("mission", text, mission);
    },
    [addMessage],
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
    setThinking(false);
  }, []);

  const conversationStarted = useMemo(
    () => messages.length > 0,
    [messages],
  );

  return {
    messages,
    conversationStarted,

    isThinking,
    setThinking,

    addUserMessage,
    addAssistantMessage,
    addSystemMessage,
    addMissionMessage,
    updateMissionMessage,
    clearConversation,
  };
}
