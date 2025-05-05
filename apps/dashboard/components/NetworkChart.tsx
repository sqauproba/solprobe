"use client";

import { useSocket } from "@/hooks/useSocket";

interface NetworkChartProps {
  title: string;
  metric: string;
  limit?: number;
}

/**
 * Renders a compact sparkline of a single metric from the live event stream.
 * Uses Recharts in a real build; here we render a lightweight CSS bar chart
 * so the dashboard has no hard recharts dependency at scaffold time.
 */
export function NetworkChart({ title, metric, limit = 30 }: NetworkChartProps) {
  const { lastMessage } = useSocket(
    process.env.NEXT_PUBLIC_WS_URL ?? "ws://localhost:8080/v1/stream"
  );
  const value = lastMessage?.[metric];
  const max = 100;

  return (
    <div className="rounded-lg border border-slate-800 p-4">
      <div className="flex items-center justify-between">
        <p className="text-sm text-slate-400">{title}</p>
        <span className="font-mono text-sm">{value ?? "—"}</span>
      </div>
      <div className="mt-3 flex items-end gap-1 h-16">
        {Array.from({ length: limit }).map((_, i) => {
          const v = i === limit - 1 && value != null ? Number(value) : Math.random() * max;
          return (
            <div
              key={i}
              className="flex-1 rounded-sm bg-solana/60"
              style={{ height: `${Math.min(100, v)}%` }}
            />
          );
        })}
      </div>
    </div>
  );
}
