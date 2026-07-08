import { useEffect, useState } from "react";
import { getInventory, type InventoryResponse } from "../api/inventory";

export function useInventory() {
  const [inventory, setInventory] = useState<InventoryResponse | null>(null);

  async function refresh() {
    try {
      const data = await getInventory();
      setInventory(data);
    } catch (e) {
      console.error(e);
    }
  }

  useEffect(() => {
    refresh();
    const t = setInterval(refresh, 15000);
    return () => clearInterval(t);
  }, []);

  return inventory;
}
