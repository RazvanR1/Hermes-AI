import { useEffect, useState } from "react";
import { getHealth, type LiveHealth } from "../api/health";

export function useHealth() {
  const [health, setHealth] = useState<LiveHealth | null>(null);

  async function refresh() {
    try {
      setHealth(await getHealth());
    } catch (e) {
      console.error(e);
    }
  }

  useEffect(() => {
    refresh();
    const t = setInterval(refresh, 5000);
    return () => clearInterval(t);
  }, []);

  return health;
}
