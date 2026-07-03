import { useEffect, useState } from "react";
import { getDashboard } from "../api/dashboard";
import type { DashboardResponse } from "../types/dashboard";

export function useDashboard() {
  const [data, setData] = useState<DashboardResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<unknown>(null);

  async function refresh() {
    try {
      setLoading(true);
      const dashboard = await getDashboard();
      setData(dashboard);
      setError(null);
    } catch (err) {
      setError(err);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    refresh();

    const timer = setInterval(refresh, 30000);

    return () => clearInterval(timer);
  }, []);

  return {
    data,
    loading,
    error,
    refresh,
  };
}
