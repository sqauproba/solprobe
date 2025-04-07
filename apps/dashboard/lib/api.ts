const BASE = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8080";

async function request<T>(path: string): Promise<T> {
  const res = await fetch(`${BASE}${path}`);
  if (!res.ok) throw new Error(`API ${res.status} for ${path}`);
  return res.json() as Promise<T>;
}

export function getHealth() {
  return request<{
    status: string;
    score: number;
    services: Record<string, string>;
    version: string;
    timestamp: string;
  }>("/v1/health");
}

export function getLatestSlot() {
  return request<{ slot: number; status: string; processed: boolean }>(
    "/v1/slots/latest"
  );
}

export function getNetwork() {
  return request<{
    tps: number;
    slot_time_ms: number;
    skip_rate: number;
    slot_count: number;
  }>("/v1/network");
}

export function getWallet(address: string) {
  return request<{
    address: string;
    lamports: number;
    sol_balance: string;
    recent_activity: { signature: string; slot: number; status: string }[];
  }>(`/v1/wallets/${encodeURIComponent(address)}`);
}

export function getBenchmark(endpoint?: string) {
  const qs = endpoint ? `?endpoint=${encodeURIComponent(endpoint)}` : "";
  return request<{ endpoint: string; latency_ms: number; p95_ms: number }>(
    `/v1/rpc/benchmark${qs}`
  );
}
