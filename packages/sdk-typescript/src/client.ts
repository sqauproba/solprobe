export interface HealthResponse {
  status: string;
  score: number;
  services: Record<string, string>;
}

export class SolProbeClient {
  private base: string;
  private apiKey?: string;

  constructor(base: string, apiKey?: string) {
    this.base = base.replace(/\/$/, "");
    this.apiKey = apiKey;
  }

  private async get<T>(path: string): Promise<T> {
    const headers: Record<string, string> = {};
    if (this.apiKey) headers["Authorization"] = `Bearer ${this.apiKey}`;
    const res = await fetch(`${this.base}${path}`, { headers });
    if (!res.ok) throw new Error(`SolProbe API error: ${res.status}`);
    return res.json() as Promise<T>;
  }

  health(): Promise<HealthResponse> {
    return this.get("/v1/health");
  }

  latestSlot(): Promise<{ slot: number; status: string }> {
    return this.get("/v1/slots/latest");
  }
}
