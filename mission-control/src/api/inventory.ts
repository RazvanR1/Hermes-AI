import { api } from "./client";

export interface InventoryResponse {
  inventory: {
    summary: {
      nodes: number;
      vms: number;
      lxc: number;
      running: number;
      stopped: number;
    };
    nodes: any[];
  };
}

export async function getInventory(): Promise<InventoryResponse> {
  const res = await api.get("/inventory");
  return res.data.data;
}
