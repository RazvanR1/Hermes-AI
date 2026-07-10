import { useCallback, useEffect, useRef, useState } from "react";
import { getDashboard } from "../api/dashboard";
import type { DashboardResponse } from "../types/dashboard";

export function useDashboard() {
  const [data, setData] = useState<DashboardResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [error, setError] = useState<unknown>(null);

  const mountedRef = useRef(true);
  const hasLoadedRef = useRef(false);

  const refresh = useCallback(async () => {
    const isInitialLoad = !hasLoadedRef.current;

    try {
      if (isInitialLoad) {
        setLoading(true);
      } else {
        setRefreshing(true);
      }

      const dashboard = await getDashboard();

      if (!mountedRef.current) return;

      setData(dashboard);
      setError(null);
      hasLoadedRef.current = true;
    } catch (err) {
      if (!mountedRef.current) return;

      setError(err);
    } finally {
      if (!mountedRef.current) return;

      setLoading(false);
      setRefreshing(false);
    }
  }, []);

  useEffect(() => {
    mountedRef.current = true;

    void refresh();

    const timer = window.setInterval(() => {
      void refresh();
    }, 30_000);

    return () => {
      mountedRef.current = false;
      window.clearInterval(timer);
    };
  }, [refresh]);

  return {
    data,
    loading,
    refreshing,
    error,
    refresh,
  };
}
