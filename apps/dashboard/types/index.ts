export interface SlotEvent {
  slot: number;
  parent?: number;
  root?: number;
}

export interface NetworkMetrics {
  tps: number;
  slotTimeMs: number;
  skipRate: number;
}

export interface HealthResponse {
  status: string;
  score: number;
  services: Record<string, string>;
}
