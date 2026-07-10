import { useEffect, useRef, useState } from "react";
import {
  getMission,
  type HermesMission,
} from "../api/missions";

const TERMINAL_STATUSES = new Set([
  "completed",
  "success",
  "succeeded",
  "failed",
  "rejected",
  "blocked",
  "cancelled",
]);

interface UseMissionLiveOptions {
  missionId: string | null;
  enabled?: boolean;
  intervalMs?: number;
  onUpdate: (mission: HermesMission) => void;
}

export function useMissionLive({
  missionId,
  enabled = true,
  intervalMs = 1500,
  onUpdate,
}: UseMissionLiveOptions) {
  const [polling, setPolling] = useState(false);
  const [lastUpdated, setLastUpdated] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const callbackRef = useRef(onUpdate);
  callbackRef.current = onUpdate;

  useEffect(() => {
    if (!missionId || !enabled) {
      setPolling(false);
      return;
    }

    const activeMissionId = missionId;

    let cancelled = false;
    let timer: number | undefined;

    async function refreshMission() {
      try {
        const freshMission = await getMission(activeMissionId);

        if (cancelled) return;

        callbackRef.current(freshMission);
        setLastUpdated(new Date().toISOString());
        setError(null);

        const status = freshMission.status.toLowerCase();

        if (TERMINAL_STATUSES.has(status)) {
          setPolling(false);
          return;
        }

        timer = window.setTimeout(refreshMission, intervalMs);
      } catch (requestError) {
        if (cancelled) return;

        setError(
          requestError instanceof Error
            ? requestError.message
            : "Mission live refresh failed",
        );

        timer = window.setTimeout(refreshMission, intervalMs);
      }
    }

    setPolling(true);
    void refreshMission();

    return () => {
      cancelled = true;
      setPolling(false);

      if (timer !== undefined) {
        window.clearTimeout(timer);
      }
    };
  }, [missionId, enabled, intervalMs]);

  return {
    polling,
    lastUpdated,
    error,
  };
}
