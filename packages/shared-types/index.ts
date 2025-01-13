export interface SlotEvent {
  slot: number;
  parent?: number;
  root?: number;
}

export interface LogEvent {
  signature: string;
  logs: string[];
  err?: string;
}

export interface NetworkMetrics {
  tps: number;
  slotTimeMs: number;
  skipRate: number;
  slotCount: number;
}
