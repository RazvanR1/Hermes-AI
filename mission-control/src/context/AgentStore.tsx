import { createContext, useContext, useState } from "react";
import type { ReactNode } from "react";

export type AgentRuntime = {
  name: string;
  status: string;
  task: string;
  progress: number;
  tone: string;
};

type AgentStoreContextType = {
  runtime: Record<string, AgentRuntime>;
  updateAgent: (
    name: string,
    patch: Partial<AgentRuntime>
  ) => void;
  resetAgents: () => void;
};

const defaultRuntime: Record<string, AgentRuntime> = {
  Guardian: {
    name: "Guardian",
    status: "running",
    task: "Scanning infrastructure",
    progress: 98,
    tone: "success",
  },
  Planner: {
    name: "Planner",
    status: "ready",
    task: "Waiting for mission",
    progress: 100,
    tone: "primary",
  },
  Reasoner: {
    name: "Reasoner",
    status: "analyzing",
    task: "Evaluating system health",
    progress: 84,
    tone: "purple",
  },
  Research: {
    name: "Research",
    status: "idle",
    task: "Standing by",
    progress: 34,
    tone: "warning",
  },
  Executor: {
    name: "Executor",
    status: "waiting",
    task: "Waiting for approval",
    progress: 0,
    tone: "muted",
  },
};

const AgentStoreContext = createContext<AgentStoreContextType | null>(null);

export function AgentStoreProvider({ children }: { children: ReactNode }) {
  const [runtime, setRuntime] = useState(defaultRuntime);

  function updateAgent(name: string, patch: Partial<AgentRuntime>) {
    setRuntime((current) => ({
      ...current,
      [name]: {
        ...current[name],
        ...patch,
      },
    }));
  }

  function resetAgents() {
    setRuntime(defaultRuntime);
  }

  return (
    <AgentStoreContext.Provider value={{ runtime, updateAgent, resetAgents }}>
      {children}
    </AgentStoreContext.Provider>
  );
}

export function useAgentStore() {
  const ctx = useContext(AgentStoreContext);

  if (!ctx) {
    throw new Error("useAgentStore must be used inside AgentStoreProvider");
  }

  return ctx;
}
