import { useEffect, useState } from "react";
import { getMissionLog, type MissionEvent } from "../api/missionlog";

export function useMissionLog() {
  const [events, setEvents] = useState<MissionEvent[]>([]);

  async function refresh() {
    try {
      setEvents(await getMissionLog());
    } catch (err) {
      console.error(err);
    }
  }

  useEffect(() => {
    refresh();
    const t = setInterval(refresh, 1000);
    return () => clearInterval(t);
  }, []);

  return events;
}
